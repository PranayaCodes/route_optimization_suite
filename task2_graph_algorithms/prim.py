"""
Prim's algorithm - builds a Minimum Spanning Tree by starting at one node
and greedily growing outward, always grabbing the cheapest edge that
connects the tree to a new node.

Needs an undirected graph, so this uses build_nepal_graph(directed=False)
from nepal_network.py instead of the directed version Dijkstra uses.

Basically the same "keep a heap of frontier options, pop the cheapest"
pattern as Dijkstra, just relaxing edge weight instead of total path
distance from the source - which is why I'm comparing the two directly
in the writeup.
"""
import heapq


def prim_mst(graph, start=None):
    if start is None:
        start = next(iter(graph.nodes))

    visited = {start}
    mst_edges = []
    total_weight = 0
    pq = []
    for v, w in graph.neighbours(start):
        heapq.heappush(pq, (w, start, v))

    build_order = [start]  # order nodes get added, for the viz

    while pq and len(visited) < graph.num_nodes():
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue  # already in the tree, this edge would make a cycle
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w
        build_order.append(v)
        for nxt, nw in graph.neighbours(v):
            if nxt not in visited:
                heapq.heappush(pq, (nw, v, nxt))

    connected = len(visited) == graph.num_nodes()
    return mst_edges, total_weight, build_order, connected