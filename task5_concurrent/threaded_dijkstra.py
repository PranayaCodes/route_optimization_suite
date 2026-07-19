"""
Threaded version of multi-source Dijkstra, using Python's threading
module (the brief's "equivalent threading library" to pthreads).

Setup: a thread-safe Queue holds all the source cities that still need
processing - each worker thread just loops, pulling one source off the
queue, running sequential Dijkstra on it (no shared state needed during
the actual computation - each Dijkstra run only touches its own local
dist/parent/visited), and then writing its result into a shared
results dict.

Critical section: the shared results dict is the only place multiple
threads could actually collide - two threads finishing at nearly the
same time could both try to write in a way that corrupts the dict's
internal state. A threading.Lock (mutex) guards every write to it, so
only one thread is ever inside that block at a time.

The work queue itself (queue.Queue) is also protecting shared state
internally using a lock + condition variable - that's what makes
.get()/.put() safe to call from multiple threads without any extra
code here. Worth pointing out since the brief asks specifically about
synchronisation primitives: this project ends up using a Lock
explicitly (for the results dict) and a Queue's internal
condition-variable-based locking implicitly (for work distribution).

Important honesty note: CPython has a Global Interpreter Lock (GIL) -
only one thread can actually execute Python bytecode at a time, no
matter how many threads exist. This means a CPU-bound workload like
Dijkstra (all Python-level computation, no I/O waiting) will NOT get
real parallel speedup from threading the way it would in C with
pthreads. This isn't a bug in this code - it's a fundamental property
of CPython. See multiprocessing_dijkstra.py for what happens once the
GIL is actually bypassed.
"""
import sys
import os
import time
import threading
import queue

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))
from dijkstra import dijkstra


def threaded_multi_source(graph, sources, num_threads):
    work_queue = queue.Queue()
    for s in sources:
        work_queue.put(s)

    results = {}
    results_lock = threading.Lock()  # the mutex protecting `results`

    def worker():
        while True:
            try:
                source = work_queue.get_nowait()
            except queue.Empty:
                return  # no more work, this thread is done

            dist, parent, order = dijkstra(graph, source)  # no shared state touched here

            with results_lock:               # critical section starts
                results[source] = dist        # only one thread in here at a time
                                               # critical section ends

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return results


if __name__ == "__main__":
    from large_graph import make_large_sparse_graph
    from sequential_dijkstra import sequential_multi_source

    g = make_large_sparse_graph(n=1000)
    sources = list(range(200))

    # correctness check first - threaded result must exactly match sequential
    seq_results = sequential_multi_source(g, sources)
    thr_results = threaded_multi_source(g, sources, num_threads=4)
    assert seq_results == thr_results, "threaded result doesn't match sequential - race condition bug"
    print("Threaded result matches sequential exactly - no race condition")

    for n_threads in (1, 2, 4, 8):
        start = time.perf_counter()
        threaded_multi_source(g, sources, num_threads=n_threads)
        elapsed = time.perf_counter() - start
        print(f"{n_threads} threads: {elapsed*1000:.1f}ms")