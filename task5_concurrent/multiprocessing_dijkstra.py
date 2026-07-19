"""
Same multi-source Dijkstra problem, but using multiprocessing instead
of threading. Each worker here is a separate OS process with its own
Python interpreter and its own GIL - so unlike threaded_dijkstra.py,
these actually run in parallel on multiple CPU cores.

Trade-off: processes don't share memory the way threads do, so there's
no "shared results dict protected by a lock" here - each worker
computes its own Dijkstra run and returns the result back to the main
process, which collects everything into one dict at the end. That
collection step is handled by multiprocessing.Pool itself, not by any
custom locking code - passing data between processes always goes
through serialisation (pickling), which is real overhead threading
doesn't have.

This file exists mainly for comparison - task 5 asks for pthreads or
"an equivalent threading library" specifically, so threaded_dijkstra.py
is the actual answer to the brief. This is here to show what removing
the GIL constraint actually buys, which matters a lot for the
"identify overheads" discussion.
"""
import sys
import os
import time
import multiprocessing

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from dijkstra import dijkstra

# multiprocessing on Windows/Mac needs the worker function to be
# importable at module level (can't be a closure) - graph has to be
# passed in as an argument to each call rather than captured
_worker_graph = None


def _init_worker(graph):
    global _worker_graph
    _worker_graph = graph


def _run_dijkstra(source):
    dist, parent, order = dijkstra(_worker_graph, source)
    return source, dist


def multiprocess_multi_source(graph, sources, num_processes):
    with multiprocessing.Pool(processes=num_processes, initializer=_init_worker, initargs=(graph,)) as pool:
        results_list = pool.map(_run_dijkstra, sources)
    return dict(results_list)


if __name__ == "__main__":
    from large_graph import make_large_sparse_graph
    from sequential_dijkstra import sequential_multi_source

    g = make_large_sparse_graph(n=1000)
    sources = list(range(200))

    seq_results = sequential_multi_source(g, sources)
    mp_results = multiprocess_multi_source(g, sources, num_processes=4)
    assert seq_results == mp_results, "multiprocessing result doesn't match sequential"
    print("Multiprocessing result matches sequential exactly")

    for n_procs in (1, 2, 4, 8):
        start = time.perf_counter()
        multiprocess_multi_source(g, sources, num_processes=n_procs)
        elapsed = time.perf_counter() - start
        print(f"{n_procs} processes: {elapsed*1000:.1f}ms")