from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Flexible Graph Prototype", layout="wide")
st.title("Flexible Graph Construction Prototype")
st.caption("Quick UI for proposal video demo")

root = Path(__file__).resolve().parent
results_path = root / "outputs" / "results.json"

if not results_path.exists():
    st.warning("No results found. Run: `python prototype_runner.py` first.")
    st.stop()

data = json.loads(results_path.read_text(encoding="utf-8"))
runs = data["runs"]

scenarios = sorted({r["scenario"] for r in runs})
strategies = sorted({r["strategy"] for r in runs})

col1, col2 = st.columns(2)
with col1:
    selected_scenario = st.selectbox("Scenario", scenarios)
with col2:
    selected_strategy = st.selectbox("Strategy", strategies)

row = next(
    r
    for r in runs
    if r["scenario"] == selected_scenario and r["strategy"] == selected_strategy
)

preview_rel = row.get("preview_image")
if preview_rel:
    st.subheader("Graph preview")
    # Keep preview smaller for proposal video screenshots (avoid huge layout jumps).
    st.image(
        root / "outputs" / preview_rel,
        use_container_width=False,
        width=650,
    )

st.subheader("Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Nodes", row["n_nodes"])
k2.metric("Edges", row["n_edges"])
k3.metric("Isolated nodes", row["isolated_nodes"])
k4.metric("Weak components", row["weak_components"])

st.subheader("Degree stats")
out_deg = row["out_degree"]
in_deg = row["in_degree"]

o1, o2, o3 = st.columns(3)
o1.metric("Out p95", f"{out_deg['p95']:.2f}")
o2.metric("Out median", f"{out_deg['median']:.2f}")
o3.metric("Out max", f"{out_deg['max']:.2f}")

i1, i2, i3 = st.columns(3)
i1.metric("In p95", f"{in_deg['p95']:.2f}")
i2.metric("In median", f"{in_deg['median']:.2f}")
i3.metric("In max", f"{in_deg['max']:.2f}")

st.subheader("Edge length + runtime")
c3, c4, c5 = st.columns(3)
edge_len = row["edge_length"]
c3.metric("Edge mean", f"{edge_len['mean']:.4f}")
c4.metric("Edge p95", f"{edge_len['p95']:.4f}")
c5.metric("Edge max", f"{edge_len['max']:.4f}")

st.metric("Runtime (s)", row["runtime_s"])

st.subheader("All runs (table)")

# Flatten dict metrics for a readable table (avoid huge json-like cells).
table_rows = []
for r in runs:
    out_deg = r["out_degree"]
    in_deg = r["in_degree"]
    edge_len = r["edge_length"]
    table_rows.append(
        {
            "scenario": r["scenario"],
            "strategy": r["strategy"],
            "runtime_s": r["runtime_s"],
            "n_nodes": r["n_nodes"],
            "n_edges": r["n_edges"],
            "isolated_nodes": r["isolated_nodes"],
            "weak_components": r["weak_components"],
            "out_deg_median": out_deg["median"],
            "out_deg_p95": out_deg["p95"],
            "in_deg_median": in_deg["median"],
            "in_deg_p95": in_deg["p95"],
            "edge_len_mean": edge_len["mean"],
            "edge_len_p95": edge_len["p95"],
        }
    )

st.dataframe(table_rows, use_container_width=True, hide_index=True)

