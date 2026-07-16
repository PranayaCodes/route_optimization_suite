"""
12-city subset of the Nepal dataset, wired up as a weighted directed
graph based roughly on the real highway network - East-West Highway
through the Terai, Prithvi Highway to Pokhara, Tribhuvan Highway down to
Hetauda, feeder roads out to Nepalgunj/Dhangadhi in the far west.

Weights are approx road distance in km (rounded, not exact - got these
from general knowledge of the highway distances, not an official source).

Roads are two-way in real life so most connections below get added as a
pair of directed edges with the same weight both ways (see graph.py for
why I kept the graph "directed" anyway).

Kept this sparse on purpose - 12 nodes, 17 road segments - because that's
roughly how the real network looks (nobody builds a direct road between
every pair of cities) and it backs up the adjacency-list choice in
graph.py.
"""
from graph import Graph

# id -> name, just for printing readable output instead of numbers
CITY_NAMES = {
    0: "Kathmandu", 1: "Pokhara", 2: "Lalitpur", 3: "Bhaktapur",
    4: "Biratnagar", 5: "Birgunj", 7: "Bharatpur", 8: "Butwal",
    9: "Dhangadhi", 10: "Janakpur", 11: "Hetauda", 12: "Nepalgunj",
}

# (u, v, distance_km) - listed once per road, expanded to both directions below
ROAD_SEGMENTS = [
    (0, 2, 6),      # Kathmandu - Lalitpur
    (0, 3, 13),     # Kathmandu - Bhaktapur
    (0, 1, 200),    # Kathmandu - Pokhara (Prithvi Highway)
    (0, 11, 135),   # Kathmandu - Hetauda (Tribhuvan Highway)
    (1, 8, 165),    # Pokhara - Butwal
    (11, 5, 90),    # Hetauda - Birgunj
    (11, 7, 75),    # Hetauda - Bharatpur
    (7, 8, 120),    # Bharatpur - Butwal
    (5, 10, 90),    # Birgunj - Janakpur (East-West Highway)
    (10, 4, 180),   # Janakpur - Biratnagar (East-West Highway)
    (8, 12, 265),   # Butwal - Nepalgunj (East-West Highway)
    (12, 9, 215),   # Nepalgunj - Dhangadhi (East-West Highway)
    (8, 5, 240),    # Butwal - Birgunj (alt East-West segment)
    (7, 5, 100),    # Bharatpur - Birgunj (direct link)
    (1, 11, 220),   # Pokhara - Hetauda (Siddhartha feeder)
    (0, 7, 146),    # Kathmandu - Bharatpur (direct)
    (3, 2, 10),     # Bhaktapur - Lalitpur
]


def build_nepal_graph(directed=True):
    """
    directed=True (what the brief wants) turns every road above into two
    directed edges with the same weight - basically simulating a normal
    two-way road while still technically being a directed graph.

    directed=False skips that and just uses a real undirected graph -
    only used for Prim's MST since MST doesn't make sense on a directed
    graph.
    """
    g = Graph(directed=directed)
    for u, v, w in ROAD_SEGMENTS:
        g.add_edge(u, v, w)
        if directed:
            g.add_edge(v, u, w)
    return g


if __name__ == "__main__":
    g = build_nepal_graph(directed=True)
    print(f"Nodes: {g.num_nodes()}, Directed edges: {g.num_edges()}")
    print(f"Underlying road segments (undirected): {len(ROAD_SEGMENTS)}")