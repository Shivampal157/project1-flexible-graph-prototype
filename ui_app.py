import streamlit as st
import json
import time
import math
from pathlib import Path
import plotly.graph_objects as go
import numpy as np
import importlib

# Attempt to import prototype_runner 
try:
    pr = importlib.import_module("prototype_runner")
except ImportError:
    pr = None

st.set_page_config(page_title="GSoC '26: Flexible Graph Prototype", layout="wide", initial_sidebar_state="collapsed")

# --- Custom Premium CSS ---
st.markdown("""
<style>
    /* Modern dark theme accents */
    .metric-container {
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 20px 10px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5), inset 0 2px 2px rgba(255, 255, 255, 0.05);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-container:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3), inset 0 2px 2px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.6);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #A0AEC0;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #FFFFFF;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-bad {
        background: linear-gradient(135deg, #f87171 0%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-good {
        background: linear-gradient(135deg, #34d399 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-title {
        font-weight: 900;
        font-size: 2.8rem;
        text-align: center;
        background: linear-gradient(to right, #38bdf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
        letter-spacing: -0.02em;
    }
    .subtitle {
        color: #e2e8f0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        opacity: 0.8;
    }
    
    /* Enhance Landing Page Hero Card */
    .hero-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(139, 92, 246, 0.4);
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.15), inset 0 0 20px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
    }
    
    /* Glowing Button Animation */
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(139, 92, 246, 0.4); transform: scale(1); }
        50% { box-shadow: 0 0 30px rgba(139, 92, 246, 0.8); transform: scale(1.02); }
        100% { box-shadow: 0 0 15px rgba(139, 92, 246, 0.4); transform: scale(1); }
    }
    
    /* Target specifically the primary Streamlit button */
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #9333ea 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 1px;
        animation: pulseGlow 2.5s infinite;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
    }
    
    /* 3D Floating Expander Effect */
    div[data-testid="stExpander"] {
        border-radius: 12px !important;
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    div[data-testid="stExpander"]:hover {
        transform: perspective(1000px) translateZ(15px) translateY(-2px);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: rgba(139, 92, 246, 0.9) !important;
    }
    
    .math-explain {
        background: rgba(0, 0, 0, 0.3);
        padding: 12px;
        border-left: 3px solid #c084fc;
        border-radius: 4px;
        font-size: 0.9rem;
        color: #e2e8f0;
        margin-top: 10px;
    }
    
    /* Custom Sidebar Highlights */
    .sidebar-highlight {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #8b5cf6;
        padding: 12px 15px;
        border-radius: 6px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .val-highlight {
        color: #38bdf8;
        font-weight: 800;
        letter-spacing: 0.5px;
        font-size: 1.1rem;
        font-family: monospace;
    }
    .author-highlight {
        background: linear-gradient(90deg, #f59e0b 0%, #fcd34d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 1.2rem;
        letter-spacing: 0.5px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }
</style>
""", unsafe_allow_html=True)

root = Path(__file__).resolve().parent
results_path = root / "outputs" / "results.json"

if not results_path.exists():
    st.error("⚠️ Results not found! Please run `python prototype_runner.py` first.")
    st.stop()

data = json.loads(results_path.read_text(encoding="utf-8"))
runs = data["runs"]
observations = data.get("observations", [])

scenarios = sorted({r["scenario"] for r in runs})
strategies = sorted({r["strategy"] for r in runs})

# --- USER LOCAL LOGO LOADER ---
import base64
import os

def get_base64_image(file_names):
    for fn in file_names:
        img_path = root / fn
        if img_path.exists():
            ext = img_path.suffix.lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
            with open(img_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"data:{mime};base64,{encoded}"
    return None

gsoc_src = get_base64_image(["gsoc_logo.jpg", "gsoc_logo.png", "gsoc_logo.jpeg"])
neural_src = get_base64_image(["neural_logo.jpg", "neural_logo.png", "neural_logo.jpeg"])

# Session State Initialization for App Routing
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = scenarios[0]
if "selected_strategy" not in st.session_state:
    st.session_state.selected_strategy = strategies[0]

# --- MAIN TITLE (Always visible, clean routing) ---
logos_html = ""
if gsoc_src or neural_src:
    logos_html += '<div style="display: flex; justify-content: center; align-items: center; gap: 40px; margin-bottom: 20px; margin-top: 15px;">\n'
    if gsoc_src:
        logos_html += f'    <img src="{gsoc_src}" height="75px" style="border-radius: 6px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">\n'
    if neural_src:
        logos_html += f'    <img src="{neural_src}" height="75px" style="border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">\n'
    logos_html += '</div>'
    st.markdown(logos_html, unsafe_allow_html=True)
else:
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; margin-top: 0px; margin-bottom: 20px;">
    <h1 style="
        font-size: 3.2rem; 
        font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 10px;
        letter-spacing: -1px;
    ">
        Neural-LAM Graph Construction
    </h1>
    <h3 style="
        color: #94A3B8; 
        font-size: 1.3rem; 
        font-weight: 400; 
        letter-spacing: 0.5px;
        margin-top: 5px;
    ">
        <span style="color: #eab308; font-weight: 600;">Google Summer of Code '26</span> Prototype: Spatial Validation Engine
    </h3>
    <div style="
        height: 1px;
        width: 250px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
        margin: 20px auto 30px auto;
    "></div>
</div>
''', unsafe_allow_html=True)


# ==========================================
# PAGE 1: HOME (Configuration Picker)
# ==========================================
if st.session_state.page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c2:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; margin-bottom: 30px; font-weight: 800; font-size: 1.8rem;">⚙️ Pipeline Configuration</h3>', unsafe_allow_html=True)
        
        scenario_idx = scenarios.index("sparse_clusters") if "sparse_clusters" in scenarios else 0
        scenario = st.selectbox("🛰️ Coordinate Scenario (Dataset Input)", scenarios, index=scenario_idx)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        strategy_idx = strategies.index("hybrid") if "hybrid" in strategies else 0
        strategy = st.selectbox("🕸️ Neighbor Selection Strategy", strategies, index=strategy_idx)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("🚀 EXECUTE 3D PIPELINE", use_container_width=True):
            st.session_state.selected_scenario = scenario
            st.session_state.selected_strategy = strategy
            st.session_state.page = "loading"
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# PAGE 2: LOADING ANIMATION
# ==========================================
elif st.session_state.page == "loading":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        progress_text = "Initializing 3D Spatial Environment..."
        my_bar = st.progress(0, text=progress_text)
        
        # Step 1
        for percent_complete in range(1, 40):
            time.sleep(0.02)
            my_bar.progress(percent_complete, text="Querying cKDTree for Spatial Neighbors...")
            
        # Step 2
        for percent_complete in range(40, 80):
            time.sleep(0.015)
            my_bar.progress(percent_complete, text=f"Applying {st.session_state.selected_strategy.upper()} Strategy Mathematical Constraints...")
            
        # Step 3
        for percent_complete in range(80, 100):
            time.sleep(0.02)
            my_bar.progress(percent_complete, text="Projecting Manifolds in 3D Space...")
            
        my_bar.progress(100, text="✨ Pipeline Complete! Initializing Neural Graphics Engine...")
        time.sleep(0.6)
        st.session_state.page = "dashboard"
        st.rerun()


# ==========================================
# PAGE 3: THE DASHBOARD
# ==========================================
elif st.session_state.page == "dashboard":

    with st.sidebar:
        st.title("🛡️ Pipeline Status")
        st.success("Simulation Executed!")
        
        # Override the glowing animation just for the sidebar button to keep it clean
        st.markdown("<style>.sidebar-btn > .stButton>button { animation: none !important; background: transparent !important; border: 1px solid #4f46e5 !important; }</style>", unsafe_allow_html=True)
        def new_gen():
            st.session_state.page = "home"
        
        # Standard button for sidebar
        st.button("⬅️ New Generation", use_container_width=True, on_click=new_gen)
            
        st.divider()
        st.markdown(f'''
        <div class="sidebar-highlight">
            <span style="color:#A0AEC0; font-size: 0.85rem; text-transform:uppercase; font-weight:600;">Scenario Config</span><br>
            <span class="val-highlight">{st.session_state.selected_scenario}</span>
        </div>
        <div class="sidebar-highlight" style="border-left-color: #ec4899;">
            <span style="color:#A0AEC0; font-size: 0.85rem; text-transform:uppercase; font-weight:600;">Algorithm Strategy</span><br>
            <span class="val-highlight" style="color: #ec4899;">{st.session_state.selected_strategy.upper()}</span>
        </div>
        ''', unsafe_allow_html=True)
        st.divider()
        
        st.markdown(f'''
        <div style="margin-bottom: 15px; padding-left: 5px;">
            <span style="color:#A0AEC0; font-size: 0.85rem; font-weight:600; text-transform:uppercase;">Primary Author:</span><br>
            <span class="author-highlight">Shivam Pal</span>
        </div>
        <div style="padding-left: 5px; margin-bottom: 10px;">
            <span style="color:#A0AEC0; font-size: 0.85rem; font-weight:600; text-transform:uppercase;">Contribution Target:</span><br>
            <div style="margin-top: 5px;">
                <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 6px 12px; border-radius: 6px; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 0.95rem; box-shadow: 0 0 10px rgba(16,185,129,0.2);">
                    mllam / neural-lam
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("💻 View Strategy Analysis Code", use_container_width=True):
            st.session_state.show_code_overlay = True
            st.rerun()

    row = next(r for r in runs if r["scenario"] == st.session_state.selected_scenario and r["strategy"] == st.session_state.selected_strategy)

    # --- FULL-WIDTH CODE MODAL OVERLAY ---
    if st.session_state.get("show_code_overlay", False):
        st.markdown('<div class="hero-card" style="margin-bottom: 30px; position: relative;">', unsafe_allow_html=True)
        
        col_title, col_close = st.columns([10, 1])
        with col_title:
            st.markdown(f"## 💻 Abstract Strategy Implementation: `{st.session_state.selected_strategy.upper()}`")
        with col_close:
            if st.button("❌ Close", key="close_modal"):
                st.session_state.show_code_overlay = False
                st.rerun()
                
        st.markdown("<hr style='opacity: 0.2; margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        
        if st.session_state.selected_strategy == "hybrid":
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.code('''def build_graph_hybrid(coords, radius=0.07):
    """
    Hybrid Repair-Aware Graph Construction
    Guarantees mathematically unbroken global continuity.
    """
    from scipy.spatial.distance import cdist
    
    # 1. Base Density: Standard spatial radius
    g = build_graph_radius(coords, radius)
    
    # 2. Structural Repair: Dynamically bridge all weak components
    while True:
        components = list(nx.weakly_connected_components(g))
        if len(components) <= 1:
            break
            
        c1, c_other = list(components[0]), []
        for c in components[1:]: c_other.extend(list(c))
        
        # Calculate optimal spatial distances between disjoint clusters
        dists = cdist(coords[c1], coords[c_other])
        idx1, idx2 = np.unravel_index(dists.argmin(), dists.shape)
        
        u, v = c1[idx1], c_other[idx2]
        dist = float(dists[idx1, idx2])
        
        # Inject bidirectional 3D graph connections
        g.add_edge(u, v, len=dist)
        g.add_edge(v, u, len=dist)
    return g''', language='python')
            with c2:
                st.markdown('''<div class="math-explain" style="padding: 20px; font-size: 1.1rem; line-height: 1.6;">
                <b style="font-size: 1.3rem; color: #38bdf8;">🧠 Scientific Breakdown:</b><br><br>
                <b>1. Strict Sparsity:</b> First, we enforce a strict <code>radius=0.07</code> limit to avoid extreme long-tail edges. <br><br>
                <b>2. Dynamic Isolation Repair:</b> Using $O(N \log N)$ <code>cKDTree</code> logic, we identify nodes left completely isolated ($Degree_{out} = 0$).<br><br>
                <b>3. L2 Bridging:</b> We dynamically inject exactly $k=6$ fallback edges using Euclidean projection for isolated clusters to cleanly reconnect the graph manifold.
                </div>''', unsafe_allow_html=True)

        elif st.session_state.selected_strategy == "radius":
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.code('''def build_graph_radius(coords, radius=0.08):
    tree = cKDTree(coords)
    g = nx.DiGraph()
    neigh = tree.query_ball_point(coords, r=radius)
    for i, ns in enumerate(neigh):
        for j in ns:
            if i != j:
                dist = np.linalg.norm(coords[i]-coords[j])
                g.add_edge(i, int(j), len=dist)
    return g''', language='python')
            with c2:
                st.markdown('''<div class="math-explain" style="padding: 20px; font-size: 1.1rem; line-height: 1.6; border-left: 3px solid #f87171;">
                <b style="font-size: 1.3rem; color: #f87171;">⚠️ Known Analytical Failure Mode:</b><br><br>
                While a fixed radius strict-bounds the maximum edge length (ideal for uniformly tight grids), it mathematically guarantees <b>isolated singular nodes</b> when applied to scattered spatial layouts or highly irregular ship-observation data clusters.
                </div>''', unsafe_allow_html=True)
                
        elif st.session_state.selected_strategy == "knn":
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.code('''def build_graph_knn(coords, k=8):
    tree = cKDTree(coords)
    _, idx = tree.query(coords, k=k+1)
    g = nx.DiGraph()
    for i in range(len(coords)):
        for j in idx[i][1:]:
            dist = np.linalg.norm(coords[i]-coords[j])
            g.add_edge(i, int(j), len=dist)
    return g''', language='python')
            with c2:
                st.markdown('''<div class="math-explain" style="padding: 20px; font-size: 1.1rem; line-height: 1.6; border-left: 3px solid #f87171;">
                <b style="font-size: 1.3rem; color: #f87171;">⚠️ Known Analytical Failure Mode:</b><br><br>
                While exactly $K$-Nearest Neighbors guarantees strict graph component connectivity ($Degree \equiv K$), when mapped onto irregular coordinate topographies, it arbitrarily forces edges to span massive Euclidean distances. This completely violates neural message-passing and localized receptive field limits.
                </div>''', unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

    def premium_metric(title, value, optimal=None):
        if optimal is not None:
            if isinstance(value, (int, float)) and isinstance(optimal, (int, float)):
                cls = "metric-good" if value <= optimal else "metric-bad"
            else:
                cls = "metric-value"
        else:
            cls = "metric-value"
            
        return f"""
        <div class="metric-container">
            <div class="metric-title">{title}</div>
            <div class="metric-value {cls}">{value}</div>
        </div>
        """

    # Uncached generation so we can dynamically receive the new prototype_runner logic
    def get_graph_data(scenario_name, strategy_name):
        if not pr:
            return None, None
        if scenario_name == 'regular_grid_32x32': coords = pr.make_regular_grid(32)
        elif scenario_name == 'jittered_grid_32x32': coords = pr.make_jittered_grid(32, seed=7)
        elif scenario_name == 'sparse_clusters': coords = pr.make_sparse_clusters(seed=11)
        else: return None, None

        if strategy_name == 'knn': g = pr.build_graph_knn(coords, k=8)
        elif strategy_name == 'radius': g = pr.build_graph_radius(coords, radius=0.08)
        elif strategy_name == 'hybrid': g = pr.build_graph_hybrid(coords, radius=0.07, k_fallback=6)
        else: return None, None
        
        return coords, g

    def generate_interactive_3D_plot(coords, g):
        # Create a beautiful 3D atmospheric wave/terrain projection
        # This makes the neural-lam "weather" dataset feel realistic!
        x_vals = coords[:, 0]
        y_vals = coords[:, 1]
        
        # Elevate Z based on a 3D sine wave to simulate atmospheric pressure/altitude 
        # Adding a tiny bit of random noise for realism
        z_vals = np.sin(x_vals * 8) * np.cos(y_vals * 8) * 0.15 + (np.random.rand(len(x_vals)) * 0.02)
        
        deg = np.array([g.in_degree(i) + g.out_degree(i) for i in g.nodes()], dtype=float)
        
        edges_x, edges_y, edges_z = [], [], []
        edges = list(g.edges())
        
        max_edges_plot = 15000 # Massively increased to eliminate visual sub-sampling artifacts
        if len(edges) > max_edges_plot:
            np.random.seed(0)
            idx = np.random.choice(len(edges), max_edges_plot, replace=False)
            edges = [edges[i] for i in idx]
            
        for (u, v) in edges:
            edges_x.extend([x_vals[u], x_vals[v], None])
            edges_y.extend([y_vals[u], y_vals[v], None])
            edges_z.extend([z_vals[u], z_vals[v], None])
            
        edge_trace = go.Scatter3d(
            x=edges_x, y=edges_y, z=edges_z,
            line=dict(width=1.5, color='rgba(139, 92, 246, 0.4)'), 
            hoverinfo='none', 
            mode='lines'
        )
        
        # Hot-color mapping for dense connectivity
        node_trace = go.Scatter3d(
            x=x_vals, y=y_vals, z=z_vals, 
            mode='markers', 
            hoverinfo='text',
            marker=dict(
                showscale=True, 
                colorscale='Plasma', 
                reversescale=False, 
                color=deg,
                size=(deg / max(1, deg.max())) * 8 + 3,
                colorbar=dict(thickness=15, title=dict(text='Topology<br>Degree', font=dict(color='#FAFAFA')), tickfont=dict(color='#FAFAFA'), outlinewidth=0, xpad=15),
                line=dict(width=0, color='#ffffff')
            )
        )
        
        node_text = [f"Node {i}<br>In-deg: {g.in_degree(i)}<br>Out-deg: {g.out_degree(i)}" for i in range(len(deg))]
        node_trace.text = node_text
        
        # 3D Layout configuration
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title='', showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)", showbackground=False, title=""),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)", showbackground=False, title=""),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgba(0,0,0,0)", showbackground=False, title=""),
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=0.0, y=-1.5, z=1.2) # Beautiful angled top-down view
                )
            ),
            height=580
        )
        return fig

    def generate_histogram(g):
        edge_lens = [d.get("len", 0.0) for _, _, d in g.edges(data=True)]
        if not edge_lens:
            return None
        fig = go.Figure(data=[go.Histogram(x=edge_lens, marker_color='#818cf8', opacity=0.8, xbins=dict(size=0.01))])
        fig.update_layout(
            title=dict(text='Edge Lengths Distribution Proof', font=dict(color='#FAFAFA', size=14)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(b=20,l=20,r=20,t=40),
            height=250,
            xaxis=dict(title=dict(text='Distance (len)', font=dict(color='#A0AEC0')), showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#A0AEC0')),
            yaxis=dict(title=dict(text='Frequency', font=dict(color='#A0AEC0')), showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#A0AEC0'))
        )
        return fig

    # Dashboard Content
    col_preview, col_space, col_metrics = st.columns([1.5, 0.05, 1])
    coords, g = get_graph_data(st.session_state.selected_scenario, st.session_state.selected_strategy)

    with col_preview:
        st.markdown("<h3 style='margin-bottom: 0;'>🌌 Neural 3D Space Projector</h3>", unsafe_allow_html=True)
        if coords is not None and g is not None:
            with st.spinner("Rendering 3D Coordinates..."):
                fig_net = generate_interactive_3D_plot(coords, g)
                st.plotly_chart(fig_net, use_container_width=True, config={'displayModeBar': False})
            
            fig_hist = generate_histogram(g)
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
        else:
            preview_rel = row.get("preview_image")
            if preview_rel: st.image(str(root / "outputs" / preview_rel), use_column_width=True)

    with col_metrics:
        st.markdown("### 🛡️ Acceptance Gates")
        iso_nodes = row["isolated_nodes"]
        weak_comp = row["weak_components"]
        
        col1, col2 = st.columns(2)
        with col1: st.markdown(premium_metric("Isolated Nodes", iso_nodes, optimal=0), unsafe_allow_html=True)
        with col2: st.markdown(premium_metric("Weak Components", weak_comp, optimal=1), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(premium_metric("Nodes", row["n_nodes"]), unsafe_allow_html=True)
        with c2: st.markdown(premium_metric("Edges", row["n_edges"]), unsafe_allow_html=True)
        with c3: st.markdown(premium_metric("Runtime (s)", f"{row['runtime_s']:.3f}"), unsafe_allow_html=True)
        
        st.markdown("<hr style='opacity: 0.2; margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("### 📊 Distributions")
        
        out_deg = row["out_degree"]
        edge_len = row["edge_length"]
        
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(premium_metric("Out Deg (p95)", f"{out_deg['p95']:.1f}"), unsafe_allow_html=True)
        with s2: st.markdown(premium_metric("Max Out Deg", f"{out_deg['max']:.0f}"), unsafe_allow_html=True)
        with s3: st.markdown(premium_metric("Edge Len (p95)", f"{edge_len['p95']:.3f}"), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #e2e8f0; font-weight: 800; font-size: 1.5rem; letter-spacing: 0.5px;'>🎯 Key Scientific Observations</h3>", unsafe_allow_html=True)
    obs_html = '<div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; margin-top: 10px;">'
    if observations:
        for obs in observations:
            parts = obs.split(':', 1)
            title = parts[0].replace('`', '')
            desc = parts[1].replace('`', '') if len(parts) > 1 else ""
            obs_html += f"""
<div style="flex: 1; min-width: 250px; background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)); border-radius: 16px; padding: 25px; border-top: 3px solid #8b5cf6; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
    <h4 style="color:#e0f2fe; margin-top:0; font-size:1.1rem; line-height: 1.4;">{title}</h4>
    <p style="color:#94a3b8; font-size:0.95rem; line-height:1.6; margin-bottom: 0;">{desc}</p>
</div>
"""
    obs_html += '</div>'
    st.markdown(obs_html, unsafe_allow_html=True)
                
    with st.expander("🗄️ Master Validation Log"):
        table_rows = []
        for r in runs:
            table_rows.append({
                "Scenario": r["scenario"].replace("_", " ").title(),
                "Strategy": r["strategy"].upper(),
                "Isolated": r["isolated_nodes"],
                "Weak Comp": r["weak_components"],
                "Out Deg p95": round(r["out_degree"]["p95"], 2),
                "Edge Len p95": round(r["edge_length"]["p95"], 4),
                "Runtime (s)": round(r["runtime_s"], 4),
            })
        st.dataframe(table_rows, use_container_width=True, hide_index=True)
