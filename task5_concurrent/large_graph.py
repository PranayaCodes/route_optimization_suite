
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from graph import Graph

random.seed(21)


def make_large_sparse_graph(n=2000, edge_factor=3, weight_range=(1, 200)):
    g = Graph(directed=True)
    for i in range(n):
        g.add_node(i)

    # guarantee connectivity first (random spanning path), same trick
    # used in task2's benchmark
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(n - 1):
        w = random.randint(*weight_range)
        g.add_edge(nodes[i], nodes[i + 1], w)

    target_edges = n * edge_factor
    added = n - 1
    attempts = 0
    max_attempts = target_edges * 10
    while added < target_edges and attempts < max_attempts:
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        attempts += 1
        if u == v:
            continue
        w = random.randint(*weight_range)
        g.add_edge(u, v, w)
        added += 1

    return g


if __name__ == "__main__":
    g = make_large_sparse_graph()
    print(f"Built test graph: {g.num_nodes()} nodes, {g.num_edges()} edges")