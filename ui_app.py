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

st.subheader("Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Nodes", row["n_nodes"])
k2.metric("Edges", row["n_edges"])
k3.metric("Isolated nodes", row["isolated_nodes"])
k4.metric("Weak components", row["weak_components"])

st.subheader("Degree stats")
c1, c2 = st.columns(2)
with c1:
    st.json({"out_degree": row["out_degree"]})
with c2:
    st.json({"in_degree": row["in_degree"]})

st.subheader("Edge length + runtime")
c3, c4 = st.columns(2)
with c3:
    st.json({"edge_length": row["edge_length"]})
with c4:
    st.metric("Runtime (s)", row["runtime_s"])

st.subheader("All runs (table)")
st.dataframe(runs, use_container_width=True)

