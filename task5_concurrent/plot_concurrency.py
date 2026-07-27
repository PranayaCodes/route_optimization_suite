"""
Plots speedup vs thread/process count. Whatever results_concurrency.csv
contains is whatever machine actually ran benchmark_concurrency.py -
run that first on a real multi-core machine to get a plot that shows
real scaling instead of flat/declining lines.
"""
import csv
import os
import matplotlib.pyplot as plt

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")

rows = []
with open(os.path.join(_THIS_DIR, "results_concurrency.csv")) as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({k: float(v) for k, v in r.items()})

workers = [r["n_workers"] for r in rows]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(workers, [r["threaded_speedup"] for r in rows], "o-", label="Threading", color="#1f77b4")
ax1.plot(workers, [r["multiprocess_speedup"] for r in rows], "s-", label="Multiprocessing", color="#d62728")
ax1.plot(workers, workers, "--", label="Ideal linear speedup", color="gray", alpha=0.5)
ax1.set_xlabel("Number of workers")
ax1.set_ylabel("Speedup (vs sequential)")
ax1.set_title("Speedup vs Worker Count")
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(workers, [r["threaded_ms"] for r in rows], "o-", label="Threading", color="#1f77b4")
ax2.plot(workers, [r["multiprocess_ms"] for r in rows], "s-", label="Multiprocessing", color="#d62728")
ax2.axhline(rows[0]["sequential_ms"], linestyle="--", color="gray", alpha=0.5, label="Sequential baseline")
ax2.set_xlabel("Number of workers")
ax2.set_ylabel("Runtime (ms)")
ax2.set_title("Raw Runtime vs Worker Count")
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_concurrency_speedup.png"), dpi=150)
print(f"Saved fig_concurrency_speedup.png to {_FIGURES_DIR}/")