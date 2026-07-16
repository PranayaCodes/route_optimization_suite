"""
Weighted directed graph using an adjacency list.

Went with adjacency list instead of a matrix because the actual road
network is sparse - a city only connects to a few neighbours, not to
every other city. Adjacency list is O(V+E) space, matrix would be O(V^2)
even though most of that matrix would just be empty/zero entries wasting
memory. Also when you loop over a node's neighbours in Dijkstra/Prim you
only touch real edges instead of scanning a whole row checking for
non-zero entries.

Graph is directed by default since some mountain roads probably aren't
equal cost both ways (uphill vs downhill), but most of the actual roads
I used are just added as two directed edges with the same weight, which
is basically the same as an undirected edge - costs nothing extra to do
it this way.
"""

from collections import defaultdict


class Graph:
    def __init__(self, directed=True):
        self.directed = directed
        self.adj = defaultdict(list)   # city_id -> [(neighbour_id, weight), ...]
        self.nodes = set()

    def add_node(self, city_id):
        self.nodes.add(city_id)
        if city_id not in self.adj:
            self.adj[city_id] = []

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def edges(self):
        # dedupe so undirected edges don't get returned twice
        seen = set()
        result = []
        for u in self.adj:
            for v, w in self.adj[u]:
                key = (u, v) if self.directed else tuple(sorted((u, v)))
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def num_edges(self):
        total = sum(len(v) for v in self.adj.values())
        return total if self.directed else total // 2

    def num_nodes(self):
        return len(self.nodes)

    def neighbours(self, u):
        return self.adj[u]