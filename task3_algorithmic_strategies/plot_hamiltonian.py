import csv
import os
import matplotlib.pyplot as plt

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")

rows = []
with open(os.path.join(_THIS_DIR, "results_hamiltonian.csv")) as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

ns = [int(r["n"]) for r in rows]
bt_explored = [int(r["backtracking_nodes_explored"]) for r in rows]
bf_checked = [int(r["bruteforce_permutations_checked"]) if r["bruteforce_permutations_checked"] not in (None, "", "None") else None for r in rows]

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.plot(ns, bt_explored, "o-", label="Backtracking (with pruning)", color="#2ca02c")

bf_ns = [n for n, v in zip(ns, bf_checked) if v is not None]
bf_vals = [v for v in bf_checked if v is not None]
ax.plot(bf_ns, bf_vals, "s-", label="Brute force (all permutations)", color="#d62728")

ax.set_yscale("log")
ax.set_xlabel("Number of cities (n)")
ax.set_ylabel("Search states examined (log scale)")
ax.set_title("Hamiltonian Path: Pruning vs Brute Force Search Space")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_hamiltonian_pruning.png"), dpi=150)
print(f"Saved fig_hamiltonian_pruning.png to {_FIGURES_DIR}/")