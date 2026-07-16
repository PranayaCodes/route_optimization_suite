import csv
import os
import matplotlib.pyplot as plt

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")

rows = []
with open(os.path.join(_THIS_DIR, "results_vrptw_synthetic.csv")) as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({k: float(v) for k, v in r.items()})

ns = [r["n_customers"] for r in rows]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(ns, [r["greedy_distance"] for r in rows], "o-", label="Greedy construction", color="#d62728")
ax1.plot(ns, [r["two_opt_distance"] for r in rows], "s-", label="Greedy + 2-opt", color="#2ca02c")
ax1.set_xlabel("Number of customers")
ax1.set_ylabel("Total route distance (units)")
ax1.set_title("Solution Quality: Greedy vs Greedy+2-opt")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(ns, [r["greedy_time_ms"] for r in rows], "o-", label="Greedy construction", color="#d62728")
ax2.plot(ns, [r["two_opt_time_ms"] for r in rows], "s-", label="Greedy + 2-opt", color="#2ca02c")
ax2.set_xlabel("Number of customers")
ax2.set_ylabel("Runtime (ms)")
ax2.set_title("Runtime Cost of Adding 2-opt")
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_vrptw_heuristics.png"), dpi=150)
print(f"Saved fig_vrptw_heuristics.png to {_FIGURES_DIR}/")