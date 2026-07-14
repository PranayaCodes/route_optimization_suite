"""
Benchmarks Dijkstra, Prim, and Bellman-Ford on synthetic sparse and dense
graphs, at a few different sizes, and times them for real.

"Sparse" here means E ~ 2V (like the actual road network - each city
connects to about 2 others on average). "Dense" means E ~ V(V-1)/4, so
about a quarter of all possible edges exist - enough to actually show
the gap between Dijkstra/Prim (which do better on sparse graphs) and
Bellman-Ford (which doesn't care either way since it just loops over
every edge regardless of structure).

This is the "big vs practical" complexity story for task 2, same idea
as the sorted-vs-random BST thing in task 1.
"""
import random
import time
import csv
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from graph import Graph
from dijkstra import dijkstra
from prim import prim_mst
from bellman_ford import bellman_ford

random.seed(7)


def make_random_graph(n, edge_factor, directed=True, weight_range=(1, 200)):
    """
    edge_factor controls how many edges get added, roughly:
      sparse ~ 2  ->  E ~ 2n
      dense  ~ n/4 -> E ~ n^2/4
    """
    g = Graph(directed=directed)
    for i in range(n):
        g.add_node(i)

    target_edges = int(n * edge_factor)
    added = 0
    attempts = 0
    max_attempts = target_edges * 20  # avoid infinite loop if graph is basically full already

    # first guarantee the graph is connected (a random spanning path),
    # then add extra random edges on top - otherwise a random sparse
    # graph is very likely to end up with unreachable nodes
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(n - 1):
        w = random.randint(*weight_range)
        g.add_edge(nodes[i], nodes[i + 1], w)
        added += 1

    while added < target_edges and attempts < max_attempts:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        attempts += 1
        if u == v:
            continue
        w = random.randint(*weight_range)
        g.add_edge(u, v, w)
        added += 1

    return g


def time_it(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def run_benchmark(sizes=(50, 200, 800)):
    rows = []
    for n in sizes:
        sparse = make_random_graph(n, edge_factor=2, directed=True)
        dense = make_random_graph(n, edge_factor=n // 4 if n // 4 > 2 else 4, directed=True)

        sparse_undirected = make_random_graph(n, edge_factor=2, directed=False)
        dense_undirected = make_random_graph(n, edge_factor=n // 4 if n // 4 > 2 else 4, directed=False)

        _, dij_sparse_t = time_it(lambda: dijkstra(sparse, 0))
        _, dij_dense_t = time_it(lambda: dijkstra(dense, 0))

        _, prim_sparse_t = time_it(lambda: prim_mst(sparse_undirected, 0))
        _, prim_dense_t = time_it(lambda: prim_mst(dense_undirected, 0))

        _, bf_sparse_t = time_it(lambda: bellman_ford(sparse, 0))
        _, bf_dense_t = time_it(lambda: bellman_ford(dense, 0))

        rows.append({
            "n": n,
            "sparse_edges": sparse.num_edges(),
            "dense_edges": dense.num_edges(),
            "dijkstra_sparse_ms": dij_sparse_t * 1000,
            "dijkstra_dense_ms": dij_dense_t * 1000,
            "prim_sparse_ms": prim_sparse_t * 1000,
            "prim_dense_ms": prim_dense_t * 1000,
            "bellman_ford_sparse_ms": bf_sparse_t * 1000,
            "bellman_ford_dense_ms": bf_dense_t * 1000,
        })
    return rows


if __name__ == "__main__":
    results = run_benchmark()
    with open(os.path.join(_THIS_DIR, "results_task2.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(f"\n--- n = {r['n']} (sparse E={r['sparse_edges']}, dense E={r['dense_edges']}) ---")
        for k, v in r.items():
            if k not in ("n", "sparse_edges", "dense_edges"):
                print(f"  {k}: {v:.4f}")