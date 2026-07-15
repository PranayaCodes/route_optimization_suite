"""
Compares backtracking-with-pruning against plain brute-force permutation
search for Hamiltonian path, on random graphs of growing size.

Point of this: brute force is O((n-1)!) no matter what the graph looks
like - it builds full permutations first and checks validity after.
Backtracking is also exponential in the worst case (a complete graph
gives it nowhere to prune), but on a graph that isn't fully connected,
it can bail out of a branch the moment it hits a dead end, way before
building a full-length candidate. This is the number that should show
pruning actually doing something.
"""
import random
import time
import csv
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from hamiltonian_backtracking import hamiltonian_path_backtracking, hamiltonian_path_bruteforce

random.seed(3)


def make_graph_with_hampath(n, extra_edge_prob=0.3):
    """
    Guarantees a Hamiltonian path exists by first wiring up a random
    permutation as a path (0-1-2-...-n-1 after shuffling labels), then
    adding some extra random edges on top so the graph isn't literally
    just a straight line (a straight line gives backtracking nothing to
    prune around, which would make it look artificially good).
    """
    order = list(range(n))
    random.shuffle(order)
    edges = set()
    for i in range(n - 1):
        edges.add(tuple(sorted((order[i], order[i + 1]))))

    # sprinkle in extra edges
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) not in edges and random.random() < extra_edge_prob:
                edges.add((u, v))

    return list(edges)


def run_benchmark(sizes=(5, 7, 9, 11)):
    rows = []
    for n in sizes:
        edges = make_graph_with_hampath(n)

        start = time.perf_counter()
        path_bt, explored_bt = hamiltonian_path_backtracking(n, edges, start=0)
        t_bt = time.perf_counter() - start

        # brute force gets slow fast, skip it for bigger n so this
        # doesn't take forever to run
        if n <= 10:
            start = time.perf_counter()
            path_bf, explored_bf = hamiltonian_path_bruteforce(n, edges, start=0)
            t_bf = time.perf_counter() - start
        else:
            explored_bf, t_bf = None, None

        rows.append({
            "n": n,
            "edges": len(edges),
            "backtracking_nodes_explored": explored_bt,
            "backtracking_time_ms": t_bt * 1000,
            "bruteforce_permutations_checked": explored_bf,
            "bruteforce_time_ms": t_bf * 1000 if t_bf is not None else None,
            "found_path": path_bt is not None,
        })
    return rows


if __name__ == "__main__":
    results = run_benchmark()
    with open(os.path.join(_THIS_DIR, "results_hamiltonian.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(f"\n--- n = {r['n']} (edges={r['edges']}, path found={r['found_path']}) ---")
        print(f"  backtracking explored: {r['backtracking_nodes_explored']} nodes, {r['backtracking_time_ms']:.4f}ms")
        if r['bruteforce_permutations_checked'] is not None:
            print(f"  brute force checked:   {r['bruteforce_permutations_checked']} permutations, {r['bruteforce_time_ms']:.4f}ms")
        else:
            print(f"  brute force: skipped (too slow at this n)")