import csv
import os
import matplotlib.pyplot as plt

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")

rows = []
with open(os.path.join(_THIS_DIR, "results_task2.csv")) as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({k: float(v) for k, v in r.items()})

ns = [r["n"] for r in rows]

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.plot(ns, [r["dijkstra_dense_ms"] for r in rows], "o-", label="Dijkstra (dense)", color="#1f77b4")
ax.plot(ns, [r["dijkstra_sparse_ms"] for r in rows], "o--", label="Dijkstra (sparse)", color="#1f77b4", alpha=0.5)
ax.plot(ns, [r["bellman_ford_dense_ms"] for r in rows], "s-", label="Bellman-Ford (dense)", color="#d62728")
ax.plot(ns, [r["bellman_ford_sparse_ms"] for r in rows], "s--", label="Bellman-Ford (sparse)", color="#d62728", alpha=0.5)
ax.plot(ns, [r["prim_dense_ms"] for r in rows], "^-", label="Prim (dense)", color="#2ca02c")
ax.plot(ns, [r["prim_sparse_ms"] for r in rows], "^--", label="Prim (sparse)", color="#2ca02c", alpha=0.5)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Number of nodes (n)")
ax.set_ylabel("Runtime (ms, log scale)")
ax.set_title("Dense vs Sparse: Dijkstra/Prim Pull Ahead of Bellman-Ford as Graphs Get Denser")
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_dense_vs_sparse.png"), dpi=150)
print(f"Saved fig_dense_vs_sparse.png to {_FIGURES_DIR}/")