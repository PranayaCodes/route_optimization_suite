"""
Runs the actual speedup measurements the brief asks for: sequential
baseline, then threaded and multiprocessing versions at 1, 2, 4, and 8
workers, wall-clock timed.

IMPORTANT: the actual numbers this produces depend entirely on how many
CPU cores the machine running it has. On a single-core machine (or a
sandboxed environment limited to 1 core), neither threading nor
multiprocessing will show real speedup - there's nothing to parallelise
onto. Run this on a real multi-core machine (basically any laptop from
the last ten years) to get numbers that actually demonstrate scaling.
"""
import time
import csv
import os
import sys
import multiprocessing

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from large_graph import make_large_sparse_graph
from sequential_dijkstra import sequential_multi_source
from threaded_dijkstra import threaded_multi_source
from multiprocessing_dijkstra import multiprocess_multi_source


def run_benchmark(n_nodes=1000, n_sources=200, thread_counts=(1, 2, 4, 8)):
    g = make_large_sparse_graph(n=n_nodes)
    sources = list(range(n_sources))

    print(f"Graph: {g.num_nodes()} nodes, {g.num_edges()} edges, {n_sources} Dijkstra runs")
    print(f"CPU cores available on this machine: {multiprocessing.cpu_count()}")

    start = time.perf_counter()
    sequential_multi_source(g, sources)
    seq_time = time.perf_counter() - start
    print(f"\nSequential baseline: {seq_time*1000:.1f}ms")

    rows = []
    for n_workers in thread_counts:
        start = time.perf_counter()
        threaded_multi_source(g, sources, num_threads=n_workers)
        thread_time = time.perf_counter() - start

        start = time.perf_counter()
        multiprocess_multi_source(g, sources, num_processes=n_workers)
        process_time = time.perf_counter() - start

        thread_speedup = seq_time / thread_time if thread_time else 0
        process_speedup = seq_time / process_time if process_time else 0

        rows.append({
            "n_workers": n_workers,
            "sequential_ms": seq_time * 1000,
            "threaded_ms": thread_time * 1000,
            "threaded_speedup": thread_speedup,
            "multiprocess_ms": process_time * 1000,
            "multiprocess_speedup": process_speedup,
        })
        print(f"\n{n_workers} workers:")
        print(f"  threading:      {thread_time*1000:.1f}ms  (speedup {thread_speedup:.2f}x)")
        print(f"  multiprocessing: {process_time*1000:.1f}ms  (speedup {process_speedup:.2f}x)")

    return rows


if __name__ == "__main__":
    results = run_benchmark()
    with open(os.path.join(_THIS_DIR, "results_concurrency.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved results_concurrency.csv")