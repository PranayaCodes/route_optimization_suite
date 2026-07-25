
import sys
import os
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from nepal_network import build_nepal_graph, CITY_NAMES, ROAD_SEGMENTS
from dijkstra import dijkstra, reconstruct_path
from prim import prim_mst

# ---------- palette ----------
INDIGO = "#2B3A4A"
INDIGO_SOFT = "#4A5D75"
MARIGOLD = "#E8A33D"
MARIGOLD_DEEP = "#C97F1E"
CREAM = "#FAF7F2"
STONE = "#EDE6D9"
GRAY = "#B9B2A3"

st.set_page_config(page_title="Nepal Route Optimisation Suite", page_icon="🧭", layout="wide")

# ---------- styling ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
}}
h1, h2, h3 {{
    font-family: 'Space Grotesk', sans-serif;
    color: {INDIGO};
    letter-spacing: -0.01em;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: {STONE};
    border-radius: 8px 8px 0 0;
    padding: 10px 20px;
    font-weight: 600;
}}
.stTabs [aria-selected="true"] {{
    background-color: {MARIGOLD} !important;
    color: {INDIGO} !important;
}}
.itinerary-strip {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0;
    background: {INDIGO};
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
}}
.itinerary-city {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: {CREAM};
    background: rgba(255,255,255,0.08);
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid rgba(232,163,61,0.4);
}}
.itinerary-leg {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: {MARIGOLD};
    padding: 0 12px;
    white-space: nowrap;
}}
.stat-box {{
    background: {STONE};
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}}
.stat-number {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: {MARIGOLD_DEEP};
}}
.stat-label {{
    font-size: 0.8rem;
    color: {INDIGO_SOFT};
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_layout():
    G = nx.Graph()
    for u, v, w in ROAD_SEGMENTS:
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=7, k=0.9)
    return G, pos


def draw_graph(highlight_edges, highlight_nodes_colors, title):
    G, pos = get_layout()
    fig, ax = plt.subplots(figsize=(9, 6.5))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    all_edges = [(u, v) for u, v, w in ROAD_SEGMENTS]
    highlight_set = {frozenset(e) for e in highlight_edges}
    off = [e for e in all_edges if frozenset(e) not in highlight_set]
    on = [e for e in all_edges if frozenset(e) in highlight_set]

    nx.draw_networkx_edges(G, pos, edgelist=off, ax=ax, edge_color=GRAY, width=1.2, alpha=0.6)
    nx.draw_networkx_edges(G, pos, edgelist=on, ax=ax, edge_color=MARIGOLD_DEEP, width=3.2)

    node_colors = [highlight_nodes_colors.get(n, INDIGO_SOFT) for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=750, ax=ax,
                            edgecolors=CREAM, linewidths=2)
    labels = {n: CITY_NAMES.get(n, n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color=CREAM,
                             font_weight="bold", ax=ax)

    edge_labels = {(u, v): w for u, v, w in ROAD_SEGMENTS}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7,
                                  font_color=INDIGO_SOFT, ax=ax)

    ax.set_title(title, fontsize=13, color=INDIGO, fontweight="bold", pad=14)
    ax.axis("off")
    fig.tight_layout()
    return fig


# ---------- header ----------
st.markdown(f"<h1 style='margin-bottom:0;'>🧭 Nepal Route Optimisation Suite</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{INDIGO_SOFT}; margin-top:4px;'>Interactive demo — Task 2 graph algorithms over the 12-city Nepal road network</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["🛣️  Shortest Path — Dijkstra", "🌳  Spanning Tree — Prim"])

# ---------- Dijkstra tab ----------
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Plan a route")
        city_options = {v: k for k, v in CITY_NAMES.items()}
        source_name = st.selectbox("From", sorted(city_options.keys()), index=sorted(city_options.keys()).index("Kathmandu"))
        target_name = st.selectbox("To", sorted(city_options.keys()), index=sorted(city_options.keys()).index("Dhangadhi"))
        run = st.button("Find shortest route", type="primary", use_container_width=True)

    if run or "dij_result" not in st.session_state:
        g = build_nepal_graph(directed=True)
        source, target = city_options[source_name], city_options[target_name]
        dist, parent, order = dijkstra(g, source)
        path = reconstruct_path(parent, source, target)
        st.session_state["dij_result"] = (source, target, dist, path)

    source, target, dist, path = st.session_state["dij_result"]

    if path is None:
        st.error(f"No route found between {CITY_NAMES[source]} and {CITY_NAMES[target]}.")
    else:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='stat-box'><div class='stat-number'>{dist[target]:.0f}</div><div class='stat-label'>km total</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-number'>{len(path)}</div><div class='stat-label'>cities</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-number'>{len(path_edges)}</div><div class='stat-label'>road segments</div></div>", unsafe_allow_html=True)

        # itinerary strip - the signature element
        strip_html = "<div class='itinerary-strip'>"
        for i, node in enumerate(path):
            strip_html += f"<span class='itinerary-city'>{CITY_NAMES[node]}</span>"
            if i < len(path) - 1:
                leg_dist = None
                for u, v, w in ROAD_SEGMENTS:
                    if {u, v} == {path[i], path[i + 1]}:
                        leg_dist = w
                        break
                strip_html += f"<span class='itinerary-leg'>—{leg_dist}km→</span>"
        strip_html += "</div>"
        st.markdown(strip_html, unsafe_allow_html=True)

        node_colors = {source: "#3F8F5F", target: "#B8443A"}
        for n in path[1:-1]:
            node_colors[n] = MARIGOLD_DEEP
        fig = draw_graph(path_edges, node_colors, f"Dijkstra: {CITY_NAMES[source]} → {CITY_NAMES[target]}")
        st.pyplot(fig)
        st.caption("Green = start, red = destination, gold = intermediate stop, gold line = shortest route")

# ---------- Prim tab ----------
with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Build the network")
        city_options2 = {v: k for k, v in CITY_NAMES.items()}
        start_name = st.selectbox("Start city", sorted(city_options2.keys()), index=sorted(city_options2.keys()).index("Kathmandu"), key="prim_start")
        run2 = st.button("Build minimum spanning tree", type="primary", use_container_width=True)

    if run2 or "prim_result" not in st.session_state:
        g_undirected = build_nepal_graph(directed=False)
        start = city_options2[start_name]
        mst_edges, total_weight, build_order, connected = prim_mst(g_undirected, start=start)
        st.session_state["prim_result"] = (start, mst_edges, total_weight, build_order, connected)

    start, mst_edges, total_weight, build_order, connected = st.session_state["prim_result"]

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='stat-box'><div class='stat-number'>{total_weight:.0f}</div><div class='stat-label'>km total network</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-box'><div class='stat-number'>{len(build_order)}</div><div class='stat-label'>cities connected</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='stat-box'><div class='stat-number'>{'yes' if connected else 'no'}</div><div class='stat-label'>fully connected</div></div>", unsafe_allow_html=True)

    strip_html = "<div class='itinerary-strip'>"
    for i, node in enumerate(build_order):
        strip_html += f"<span class='itinerary-city'>{CITY_NAMES[node]}</span>"
        if i < len(build_order) - 1:
            strip_html += f"<span class='itinerary-leg'>#{i+1}→</span>"
    strip_html += "</div>"
    st.markdown(strip_html, unsafe_allow_html=True)
    st.caption("Order in which Prim's algorithm attaches each city to the growing tree")

    mst_edge_pairs = [(u, v) for u, v, w in mst_edges]
    node_colors = {start: "#3F8F5F"}
    for n in build_order[1:]:
        node_colors[n] = MARIGOLD_DEEP
    fig = draw_graph(mst_edge_pairs, node_colors, f"Prim's MST from {CITY_NAMES[start]}")
    st.pyplot(fig)
    st.caption("Green = starting city, gold nodes/lines = the minimum spanning tree")

st.markdown("---")
st.caption("Route Optimisation Suite — ST5003CEM Advanced Algorithms — github.com/PranayaCodes/route_optimization_suite")