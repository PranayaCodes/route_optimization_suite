"""
Makes the "step by step" visualizations the brief asks for - one for
Dijkstra's shortest path (Kathmandu -> Dhangadhi, since that's basically
one end of the country to the other) and one for Prim's MST over the
whole network.

Using networkx just for the graph layout (spring_layout) - the actual
Dijkstra/Prim logic is from dijkstra.py / prim.py, not networkx's
built-in versions, that would defeat the point of task 2.
"""
import os
import networkx as nx
import matplotlib.pyplot as plt

from nepal_network import build_nepal_graph, CITY_NAMES, ROAD_SEGMENTS
from dijkstra import dijkstra, reconstruct_path
from prim import prim_mst

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")


def _make_nx_layout():
    # build a plain networkx graph just so we can reuse its layout
    # algorithm - positions end up consistent across all the figures
    # below, so they're actually comparable
    G = nx.Graph()
    for u, v, w in ROAD_SEGMENTS:
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=7, k=0.9)
    return G, pos


def plot_dijkstra_path(source=0, target=9):
    g = build_nepal_graph(directed=True)
    dist, parent, order = dijkstra(g, source)
    path = reconstruct_path(parent, source, target)

    G, pos = _make_nx_layout()
    path_edges = set()
    for i in range(len(path) - 1):
        path_edges.add(frozenset((path[i], path[i + 1])))

    fig, ax = plt.subplots(figsize=(9, 7))
    all_edges = [(u, v) for u, v, w in ROAD_SEGMENTS]
    on_path = [e for e in all_edges if frozenset(e) in path_edges]
    off_path = [e for e in all_edges if frozenset(e) not in path_edges]

    nx.draw_networkx_edges(G, pos, edgelist=off_path, ax=ax, edge_color="lightgray", width=1)
    nx.draw_networkx_edges(G, pos, edgelist=on_path, ax=ax, edge_color="#d62728", width=3)

    node_colors = []
    for n in G.nodes():
        if n == source:
            node_colors.append("#2ca02c")   # start = green
        elif n == target:
            node_colors.append("#d62728")   # goal = red
        elif n in path:
            node_colors.append("#ffbb78")   # on path = orange
        else:
            node_colors.append("#c7c7c7")   # not touched = gray

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax)
    labels = {n: CITY_NAMES.get(n, n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    edge_labels = {(u, v): w for u, v, w in ROAD_SEGMENTS}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)

    ax.set_title(f"Dijkstra: {CITY_NAMES[source]} -> {CITY_NAMES[target]}  "
                 f"(total {dist[target]}km, {len(path)} cities)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(_FIGURES_DIR, "fig_dijkstra_path.png"), dpi=150)
    plt.close(fig)
    print(f"Dijkstra path {CITY_NAMES[source]} -> {CITY_NAMES[target]}: "
          f"{[CITY_NAMES.get(n, n) for n in path]}, {dist[target]}km")


def plot_prim_mst(start=0):
    g_undirected = build_nepal_graph(directed=False)
    mst_edges, total_weight, build_order, connected = prim_mst(g_undirected, start=start)

    G, pos = _make_nx_layout()
    mst_edge_set = {frozenset((u, v)) for u, v, w in mst_edges}

    fig, ax = plt.subplots(figsize=(9, 7))
    all_edges = [(u, v) for u, v, w in ROAD_SEGMENTS]
    in_mst = [e for e in all_edges if frozenset(e) in mst_edge_set]
    not_in_mst = [e for e in all_edges if frozenset(e) not in mst_edge_set]

    nx.draw_networkx_edges(G, pos, edgelist=not_in_mst, ax=ax, edge_color="lightgray",
                            width=1, style="dashed")
    nx.draw_networkx_edges(G, pos, edgelist=in_mst, ax=ax, edge_color="#2ca02c", width=3)

    nx.draw_networkx_nodes(G, pos, node_color="#9ecae1", node_size=700, ax=ax)
    labels = {n: CITY_NAMES.get(n, n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    edge_labels = {(u, v): w for u, v, w in ROAD_SEGMENTS}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)

    ax.set_title(f"Prim's MST from {CITY_NAMES[start]}  "
                 f"(total {total_weight}km, connected={connected})")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(_FIGURES_DIR, "fig_prim_mst.png"), dpi=150)
    plt.close(fig)
    print(f"Prim MST total weight: {total_weight}km, "
          f"build order: {[CITY_NAMES.get(n, n) for n in build_order]}")


if __name__ == "__main__":
    plot_dijkstra_path(source=0, target=9)   # Kathmandu -> Dhangadhi
    plot_prim_mst(start=0)
    print(f"Saved figures to {_FIGURES_DIR}/")