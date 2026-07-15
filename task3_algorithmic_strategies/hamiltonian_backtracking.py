"""
Hamiltonian Path (and Cycle) - backtracking problem for task 3.

Ties back into the route-planning theme directly: a Hamiltonian path
through the city graph is a route that visits every city exactly once -
basically a simplified version of what a delivery driver covering every
city in one trip would want (without worrying about optimal cost, just
"does a valid all-cities route even exist").

Backtracking approach: build up a path city by city. At each step, only
try neighbours that are (a) actually connected by a road, and (b) not
already visited. The moment neither condition can be satisfied for any
neighbour, backtrack - that's the pruning. Compared to brute-force
"generate every permutation of cities and check if it's a valid path",
this cuts off huge chunks of the search tree early instead of building
a full invalid permutation and only checking it at the end.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from itertools import permutations


def _build_adjacency(n, edges):
    adj = {i: set() for i in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def hamiltonian_path_backtracking(n, edges, start=0):
    """
    n: number of nodes (labelled 0..n-1)
    edges: list of (u, v) undirected edges
    Returns (path or None, nodes_explored) - nodes_explored counts how
    many times the recursive function actually got called, used later
    to show how much pruning cuts down the search.
    """
    adj = _build_adjacency(n, edges)
    path = [start]
    visited = {start}
    nodes_explored = [0]  # list so the nested function can mutate it

    def backtrack():
        nodes_explored[0] += 1
        if len(path) == n:
            return True  # visited every city - done

        current = path[-1]
        for neighbour in adj[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                path.append(neighbour)
                if backtrack():
                    return True
                # didn't work out, undo and try the next neighbour
                path.pop()
                visited.remove(neighbour)
        return False

    found = backtrack()
    return (path[:] if found else None), nodes_explored[0]


def hamiltonian_cycle_backtracking(n, edges, start=0):
    """
    Same idea as the path version, but also requires the last city to
    connect back to the start - a full cycle, not just a path.
    """
    adj = _build_adjacency(n, edges)
    path = [start]
    visited = {start}
    nodes_explored = [0]

    def backtrack():
        nodes_explored[0] += 1
        if len(path) == n:
            return start in adj[path[-1]]  # can we close the loop back to start?

        current = path[-1]
        for neighbour in adj[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                path.append(neighbour)
                if backtrack():
                    return True
                path.pop()
                visited.remove(neighbour)
        return False

    found = backtrack()
    return (path[:] if found else None), nodes_explored[0]


def hamiltonian_path_bruteforce(n, edges, start=0):
    """
    Generates every permutation of the remaining n-1 cities and checks
    each one fully against the edge set - no early pruning at all. Only
    practical for small n, here purely to measure how many candidates
    get checked vs. the backtracking version above.
    """
    edge_set = set()
    for u, v in edges:
        edge_set.add((u, v))
        edge_set.add((v, u))

    others = [i for i in range(n) if i != start]
    candidates_checked = 0
    for perm in permutations(others):
        candidates_checked += 1
        full_path = [start] + list(perm)
        valid = all((full_path[i], full_path[i + 1]) in edge_set for i in range(n - 1))
        if valid:
            return full_path, candidates_checked
    return None, candidates_checked


if __name__ == "__main__":
    # small dense-ish test graph where a Hamiltonian path definitely
    # exists, just to prove the algorithm works before trying it on the
    # real (sparse) Nepal network
    n_test = 6
    test_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 2), (1, 3), (2, 4), (3, 5)]

    path, explored_bt = hamiltonian_path_backtracking(n_test, test_edges, start=0)
    print(f"Test graph - backtracking found: {path} (explored {explored_bt} nodes)")

    path_bf, explored_bf = hamiltonian_path_bruteforce(n_test, test_edges, start=0)
    print(f"Test graph - brute force found: {path_bf} (checked {explored_bf} permutations)")

    print()
    print("--- now trying the real 12-city Nepal road network ---")
    from nepal_network import ROAD_SEGMENTS, CITY_NAMES
    n_nepal = 12
    # nepal_network uses non-contiguous city ids (0-12 skipping 6), so
    # remap to 0..11 contiguous ids just for this algorithm
    real_ids = sorted(set([u for u, v, w in ROAD_SEGMENTS] + [v for u, v, w in ROAD_SEGMENTS]))
    remap = {old: new for new, old in enumerate(real_ids)}
    nepal_edges = [(remap[u], remap[v]) for u, v, w in ROAD_SEGMENTS]

    path, explored = hamiltonian_path_backtracking(len(real_ids), nepal_edges, start=remap[0])
    if path:
        named = [CITY_NAMES[real_ids[i]] for i in path]
        print(f"Hamiltonian path exists: {named}")
    else:
        print(f"No Hamiltonian path exists starting from Kathmandu "
              f"(explored {explored} partial paths before giving up) - "
              f"makes sense, the real road network is too sparse for one")