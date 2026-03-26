# Project 1 Prototype (Video-ready)

This repository contains a compact, reproducible prototype for proposal evidence for **Flexible graph construction**.

It compares multiple **coordinate regimes** (regular grid, jittered/irregular grid, sparse clusters) with multiple **graph-building strategies** (kNN, radius, hybrid), and produces a single metrics report (JSON + Markdown) that is easy to show in a short video.

Optionally, it includes a lightweight Streamlit UI to switch scenario/strategy and display key metrics.

## What it demonstrates

- Multiple coordinate regimes:
  - regular grid
  - jittered irregular grid
  - sparse clusters
- Multiple graph-building strategies:
  - knn
  - radius
  - hybrid (radius + knn fallback)
- Comparable metrics:
  - isolated nodes
  - weakly connected components
  - in/out degree statistics
  - edge-length statistics
  - runtime

## Quick run

From repo root:

```bash
python prototype_runner.py
```

Outputs:
- `outputs/results.json`
- `outputs/results.md`

## Optional UI (recommended for the demo video)

If `streamlit` is installed:

```bash
streamlit run ui_app.py
```

## Suggested video flow (2–4 min)

1. Show the three scenario types.
2. Run `prototype_runner.py` live.
3. Open `outputs/results.md` and explain one key trade-off.
4. (Optional) Open the Streamlit UI and compare one scenario across all strategies.
5. Close with what you would upstream first (tests + metric hooks, then strategy improvements).
