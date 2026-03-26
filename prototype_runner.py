from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.spatial import cKDTree


@dataclass
class Scenario:
    name: str
    coords: np.ndarray


def make_regular_grid(n_side: int = 32) -> np.ndarray:
    xs, ys = np.meshgrid(
        np.linspace(0.0, 1.0, n_side), np.linspace(0.0, 1.0, n_side)
    )
    return np.stack([xs.ravel(), ys.ravel()], axis=1)


def make_jittered_grid(
    n_side: int = 32, jitter: float = 0.015, seed: int = 0
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    coords = make_regular_grid(n_side)
    return np.clip(
        coords + rng.normal(0.0, jitter, size=coords.shape), 0.0, 1.0
    )


def make_sparse_clusters(
    n_clusters: int = 8, points_per_cluster: int = 40, seed: int = 0
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    centers = rng.uniform(0.1, 0.9, size=(n_clusters, 2))
    pts = []
    for c in centers:
        pts.append(
            np.clip(
                c + rng.normal(0.0, 0.025, size=(points_per_cluster, 2)),
                0.0,
                1.0,
            )
        )
    return np.vstack(pts)


def build_graph_knn(coords: np.ndarray, k: int = 8) -> nx.DiGraph:
    tree = cKDTree(coords)
    _, idx = tree.query(coords, k=min(k + 1, len(coords)))
    g = nx.DiGraph()
    for i, p in enumerate(coords):
        g.add_node(i, pos=p)
    for i in range(len(coords)):
        for j in idx[i][1:]:
            if i == j:
                continue
            d = float(np.linalg.norm(coords[i] - coords[j]))
            g.add_edge(i, int(j), len=d)
    return g


def build_graph_radius(
    coords: np.ndarray, radius: float = 0.08, max_neighbors: int = 24
) -> nx.DiGraph:
    tree = cKDTree(coords)
    g = nx.DiGraph()
    for i, p in enumerate(coords):
        g.add_node(i, pos=p)

    neigh = tree.query_ball_point(coords, r=radius)
    for i, ns in enumerate(neigh):
        if len(ns) > max_neighbors:
            # Keep nearest among radius neighbors (deterministic).
            ns = sorted(
                ns,
                key=lambda j: np.linalg.norm(coords[i] - coords[j]),
            )[:max_neighbors]
        for j in ns:
            if i == j:
                continue
            d = float(np.linalg.norm(coords[i] - coords[j]))
            g.add_edge(i, int(j), len=d)
    return g


def build_graph_hybrid(
    coords: np.ndarray, radius: float = 0.07, k_fallback: int = 6
) -> nx.DiGraph:
    g = build_graph_radius(coords, radius=radius)
    tree = cKDTree(coords)
    _, idx = tree.query(coords, k=min(k_fallback + 1, len(coords)))

    # Ensure no node becomes a sink due to too-small radius.
    for i in range(len(coords)):
        if g.out_degree(i) == 0:
            for j in idx[i][1:]:
                if i == j:
                    continue
                d = float(np.linalg.norm(coords[i] - coords[j]))
                g.add_edge(i, int(j), len=d)
    return g


def graph_metrics(g: nx.DiGraph) -> dict:
    n = g.number_of_nodes()
    m = g.number_of_edges()

    out_deg = np.array([g.out_degree(i) for i in g.nodes()], dtype=float)
    in_deg = np.array([g.in_degree(i) for i in g.nodes()], dtype=float)

    isolated = int(np.sum((out_deg + in_deg) == 0))
    weak_components = (
        nx.number_weakly_connected_components(g) if n > 0 else 0
    )

    edge_lens = np.array(
        [d.get("len", 0.0) for _, _, d in g.edges(data=True)],
        dtype=float,
    )

    return {
        "n_nodes": n,
        "n_edges": m,
        "isolated_nodes": isolated,
        "weak_components": int(weak_components),
        "out_degree": {
            "min": float(out_deg.min(initial=0)),
            "median": float(np.median(out_deg)) if n else 0.0,
            "p95": float(np.percentile(out_deg, 95)) if n else 0.0,
            "max": float(out_deg.max(initial=0)),
        },
        "in_degree": {
            "min": float(in_deg.min(initial=0)),
            "median": float(np.median(in_deg)) if n else 0.0,
            "p95": float(np.percentile(in_deg, 95)) if n else 0.0,
            "max": float(in_deg.max(initial=0)),
        },
        "edge_length": {
            "mean": float(edge_lens.mean()) if len(edge_lens) else 0.0,
            "p95": float(np.percentile(edge_lens, 95))
            if len(edge_lens)
            else 0.0,
            "max": float(edge_lens.max(initial=0.0)),
        },
    }


def run() -> dict:
    scenarios = [
        Scenario("regular_grid_32x32", make_regular_grid(32)),
        Scenario("jittered_grid_32x32", make_jittered_grid(32, seed=7)),
        Scenario("sparse_clusters", make_sparse_clusters(seed=11)),
    ]
    strategies = {
        "knn": lambda c: build_graph_knn(c, k=8),
        "radius": lambda c: build_graph_radius(c, radius=0.08),
        "hybrid": lambda c: build_graph_hybrid(
            c, radius=0.07, k_fallback=6
        ),
    }

    rows = []
    for sc in scenarios:
        for name, fn in strategies.items():
            t0 = time.perf_counter()
            g = fn(sc.coords)
            dt = time.perf_counter() - t0
            rows.append(
                {
                    "scenario": sc.name,
                    "strategy": name,
                    "runtime_s": round(dt, 4),
                    **graph_metrics(g),
                }
            )
    return {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "runs": rows}


def write_report(data: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8"
    )

    lines = [
        "# Flexible Graph Construction Prototype Report",
        "",
        "| scenario | strategy | nodes | edges | isolated | weak_components | out_deg_p95 | runtime (s) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for r in data["runs"]:
        lines.append(
            f"| {r['scenario']} | {r['strategy']} | {r['n_nodes']} | {r['n_edges']} | "
            f"{r['isolated_nodes']} | {r['weak_components']} | {r['out_degree']['p95']:.2f} | {r['runtime_s']:.4f} |"
        )

    (output_dir / "results.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "outputs"
    report = run()
    write_report(report, out)
    print(f"Saved report to: {out}")

