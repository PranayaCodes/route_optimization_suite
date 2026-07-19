"""
Sequential baseline - runs Dijkstra from every source city one after
another, single threaded. This is what the threaded/multiprocess
versions get compared against for speedup.

"Multi-source shortest path" is one of the examples the brief itself
gives for what to parallelise, and it's a natural fit: each source's
Dijkstra run is completely independent of every other source's run -
the only thing that ties them together is where the results get
written, which is exactly the critical section the threaded version
has to protect.
"""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from dijkstra import dijkstra


def sequential_multi_source(graph, sources):
    results = {}
    for s in sources:
        dist, parent, order = dijkstra(graph, s)
        results[s] = dist
    return results


if __name__ == "__main__":
    from large_graph import make_large_sparse_graph
    g = make_large_sparse_graph(n=1000)
    sources = list(range(200))  # run Dijkstra from 200 different starting cities

    start = time.perf_counter()
    results = sequential_multi_source(g, sources)
    elapsed = time.perf_counter() - start

    print(f"Sequential: {len(sources)} Dijkstra runs on a {g.num_nodes()}-node graph")
    print(f"Time: {elapsed*1000:.1f}ms")