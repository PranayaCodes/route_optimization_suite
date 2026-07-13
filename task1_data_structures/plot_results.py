import csv
import os
import matplotlib.pyplot as plt

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_FIGURES_DIR = os.path.join(os.path.dirname(_THIS_DIR), "figures")

rows = []
with open(os.path.join(_THIS_DIR, "results.csv")) as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({k: float(v) for k, v in r.items()})

ns = [r["n"] for r in rows]

# --- Figure 1: Search time comparison (log scale) ---
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(ns, [r["bst_sorted_search_ms"] for r in rows], "o-", label="BST (sorted insert, degenerate)", color="#d62728")
ax.plot(ns, [r["bst_random_search_ms"] for r in rows], "o-", label="BST (random insert)", color="#ff9896")
ax.plot(ns, [r["avl_random_search_ms"] for r in rows], "s-", label="AVL Tree", color="#2ca02c")
ax.plot(ns, [r["hash_search_ms"] for r in rows], "^-", label="Hash Table", color="#1f77b4")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Number of cities (n)")
ax.set_ylabel("Search time for 200 lookups (ms, log scale)")
ax.set_title("Search Performance: Theory vs Practice")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_search_comparison.png"), dpi=150)

# --- Figure 2: Tree height growth (structural evidence of degeneration) ---
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(ns, [r["bst_sorted_height"] for r in rows], "o-", label="BST height (sorted insert)", color="#d62728")
ax.plot(ns, [r["avl_sorted_height"] for r in rows], "s-", label="AVL height (sorted insert)", color="#2ca02c")
import math
ax.plot(ns, [math.log2(n) for n in ns], "--", label="log2(n) reference", color="gray")
ax.set_xscale("log")
ax.set_xlabel("Number of cities (n)")
ax.set_ylabel("Tree height")
ax.set_title("Tree Height Growth: BST Degenerates, AVL Stays O(log n)")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_height_comparison.png"), dpi=150)

# --- Figure 3: Insert time comparison across all structures ---
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(ns, [r["bst_random_insert_ms"] for r in rows], "o-", label="BST (random)")
ax.plot(ns, [r["avl_random_insert_ms"] for r in rows], "s-", label="AVL Tree")
ax.plot(ns, [r["hash_insert_ms"] for r in rows], "^-", label="Hash Table")
ax.plot(ns, [r["heap_push_ms"] for r in rows], "d-", label="Min-Heap (push)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Number of cities (n)")
ax.set_ylabel("Total insert time (ms, log scale)")
ax.set_title("Insertion Performance Across Structures")
ax.legend()
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(_FIGURES_DIR, "fig_insert_comparison.png"), dpi=150)

print(f"Saved 3 figures to {_FIGURES_DIR}/")