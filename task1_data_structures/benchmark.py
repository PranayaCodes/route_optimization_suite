"""
Runs the actual timing tests for task 1.

Testing insert + search at n = 100 / 1,000 / 10,000 cities for all four
structures:
  - BST (no balancing)
  - AVL Tree (self balancing)
  - Hash Table (chaining)
  - Min-Heap (push + pop_min - didn't bother testing "search" on this
    one since that's not really what a heap is for)

For BST and AVL I test two insertion orders - random and sorted. Sorted
order is the classic worst case for a plain BST (turns into a linked
list basically, O(n) per op instead of O(log n)) which is the whole
reason AVL trees are a thing. This comparison is honestly the most
interesting result out of all of task 1.
"""

import random
import time
import csv
import sys
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
sys.path.insert(0, _THIS_DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

from city import City
from bst import BST
from avl import AVLTree
from hash_table import HashTable
from min_heap import MinHeap

random.seed(42)


def make_cities(n, order="random"):
    ids = list(range(n))
    if order == "random":
        random.shuffle(ids)
    cities = []
    for cid in ids:
        cities.append(City(
            city_id=cid,
            name=f"City{cid}",
            lat=round(random.uniform(26.0, 30.5), 4),
            lon=round(random.uniform(80.0, 88.5), 4),
            population=random.randint(1_000, 500_000),
            distance=round(random.uniform(1, 1000), 2),
        ))
    return cities


def time_it(fn, *args):
    start = time.perf_counter()
    fn(*args)
    return time.perf_counter() - start


def bench_tree(tree_cls, cities, search_ids):
    tree = tree_cls()
    insert_time = time_it(lambda: [tree.insert(c) for c in cities])
    search_time = time_it(lambda: [tree.search(i) for i in search_ids])
    h = tree.height() if hasattr(tree, "height") else None
    return insert_time, search_time, h


def bench_hash(cities, search_ids):
    ht = HashTable()
    insert_time = time_it(lambda: [ht.insert(c) for c in cities])
    search_time = time_it(lambda: [ht.search(i) for i in search_ids])
    return insert_time, search_time


def bench_heap(cities):
    heap = MinHeap()
    push_time = time_it(lambda: [heap.push(c) for c in cities])
    n = len(heap)
    pop_time = time_it(lambda: [heap.pop_min() for _ in range(n)])
    return push_time, pop_time


def run_all(sizes=(100, 1000, 10000)):
    rows = []
    for n in sizes:
        random_cities = make_cities(n, order="random")
        sorted_cities = sorted(make_cities(n, order="random"), key=lambda c: c.city_id)
        search_sample = random.sample(range(n), min(n, 200))

        bst_r_ins, bst_r_search, bst_r_h = bench_tree(BST, random_cities, search_sample)
        bst_s_ins, bst_s_search, bst_s_h = bench_tree(BST, sorted_cities, search_sample)

        avl_r_ins, avl_r_search, avl_r_h = bench_tree(AVLTree, random_cities, search_sample)
        avl_s_ins, avl_s_search, avl_s_h = bench_tree(AVLTree, sorted_cities, search_sample)

        ht_ins, ht_search = bench_hash(random_cities, search_sample)
        heap_push, heap_pop = bench_heap(random_cities)

        rows.append({
            "n": n,
            "bst_random_insert_ms": bst_r_ins * 1000,
            "bst_random_search_ms": bst_r_search * 1000,
            "bst_random_height": bst_r_h,
            "bst_sorted_insert_ms": bst_s_ins * 1000,
            "bst_sorted_search_ms": bst_s_search * 1000,
            "bst_sorted_height": bst_s_h,
            "avl_random_insert_ms": avl_r_ins * 1000,
            "avl_random_search_ms": avl_r_search * 1000,
            "avl_random_height": avl_r_h,
            "avl_sorted_insert_ms": avl_s_ins * 1000,
            "avl_sorted_search_ms": avl_s_search * 1000,
            "avl_sorted_height": avl_s_h,
            "hash_insert_ms": ht_ins * 1000,
            "hash_search_ms": ht_search * 1000,
            "heap_push_ms": heap_push * 1000,
            "heap_pop_ms": heap_pop * 1000,
        })
    return rows


if __name__ == "__main__":
    results = run_all()
    with open(os.path.join(_THIS_DIR, "results.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(f"\n--- n = {r['n']} ---")
        for k, v in r.items():
            if k != "n":
                print(f"  {k}: {v}")