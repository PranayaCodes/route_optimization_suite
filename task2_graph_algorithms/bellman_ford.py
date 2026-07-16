"""
Bellman-Ford - like Dijkstra but handles negative edge weights, and can
also tell you if the graph has a negative cycle.

Dijkstra can't handle negative weights because it finalises a node the
moment it pops from the heap and never looks at it again - if a negative
edge shows up later that would've made an already-finalised node cheaper,
Dijkstra just misses it. Bellman-Ford avoids this by relaxing literally
every edge, V-1 times, which is enough passes to guarantee the shortest
path (as long as there's no negative cycle - a path can't be "shortest"
if you can keep looping around a negative cycle to make it cheaper
forever).

The extra V-th pass at the end checks for exactly that: if any edge can
still be relaxed after V-1 passes should have already found the true
shortest paths, that only makes sense if a negative cycle exists.
"""

def bellman_ford(graph, source):
    dist = {node: float("inf") for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[source] = 0
    edge_list = graph.edges()

    for _ in range(graph.num_nodes() - 1):
        changed = False
        for u, v, w in edge_list:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break  # nothing changed this pass, we've converged early, no need to keep going

    # one more pass - if this still finds an improvement, there's a negative cycle
    negative_cycle_nodes = set()
    for u, v, w in edge_list:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            negative_cycle_nodes.add(v)

    has_negative_cycle = len(negative_cycle_nodes) > 0
    return dist, parent, has_negative_cycle, negative_cycle_nodes