"""
Dijkstra's algorithm - shortest path from one source, only works right
if all weights are non-negative (see bellman_ford.py for why that
matters).

Using heapq as the priority queue here. Yeah I built a MinHeap from
scratch in task1 but that one's keyed on city.distance specifically for
the "closest unvisited city" use case - this needs to be keyed on
running path distance instead so it was simpler to just use heapq
directly rather than bolt on a second use case to that class.

Also keeping track of parent[] so I can actually rebuild the path
afterwards, not just print the total distance.
"""
import heapq


def dijkstra(graph, source):
    dist = {node: float("inf") for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[source] = 0
    visited = set()
    pq = [(0, source)]
    order = []  # keeps track of the order nodes got finalised - used for the step by step viz

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue  # stale entry from an earlier relax, skip it
        visited.add(u)
        order.append(u)

        for v, weight in graph.neighbours(u):
            if v in visited:
                continue
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, parent, order


def reconstruct_path(parent, source, target):
    if parent.get(target) is None and target != source:
        return None  # never got reached
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path if path[0] == source else None

