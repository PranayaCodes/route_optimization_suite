"""
VRPTW needs to know the travel cost between ANY two customers, not just
cities that have a direct road - so this runs Dijkstra from every city
once and builds a full distance matrix out of the results.

Reuses dijkstra.py from task 2 instead of writing shortest-path logic
again - this is exactly why Dijkstra was built as a reusable function in
the first place.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from nepal_network import build_nepal_graph, CITY_NAMES
from dijkstra import dijkstra


def build_distance_matrix():
    g = build_nepal_graph(directed=True)
    city_ids = sorted(g.nodes)
    matrix = {}
    for source in city_ids:
        dist, _, _ = dijkstra(g, source)
        matrix[source] = dist
    return matrix, city_ids


if __name__ == "__main__":
    matrix, city_ids = build_distance_matrix()
    print("Distance matrix (km), a few sample entries:")
    print(f"  Kathmandu -> Dhangadhi: {matrix[0][9]}km")
    print(f"  Pokhara -> Biratnagar: {matrix[1][4]}km")
    print(f"  Nepalgunj -> Bhaktapur: {matrix[12][3]}km")