"""
The real 11-customer Nepal instance turned out to be too small to show
2-opt actually improving anything - greedy's nearest-neighbour choice
happened to already be optimal for routes that short. That's a real
result worth mentioning, but it doesn't demonstrate what 2-opt is
actually for, so this generates bigger synthetic instances (random
customers on a 2D plane, straight-line distance) purely to get a
meaningful greedy-vs-2opt comparison - same idea as using synthetic
data for the n=10,000 stress test back in task 1.
"""
import random
import math
import time
import csv
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)

from vrptw_problem import route_is_feasible, route_distance, total_solution_distance
from greedy_construction import greedy_construct
from local_search import two_opt_improve

random.seed(11)


def make_synthetic_instance(num_customers, capacity=20, num_vehicles=6, speed=50, area=500):
    """
    Places the depot at the centre of a square area, customers randomly
    scattered around it. Distances are straight-line (Euclidean), which
    always satisfies the triangle inequality - unlike the real road
    network, so this is a fair, "clean" instance for testing heuristic
    behaviour without real-world road-network quirks getting in the way.
    """
    depot = (area / 2, area / 2)
    coords = {0: depot}
    customers = {}
    for i in range(1, num_customers + 1):
        x, y = random.uniform(0, area), random.uniform(0, area)
        coords[i] = (x, y)
        dist_from_depot = math.dist(depot, (x, y))
        travel_hours = dist_from_depot / speed
        demand = random.randint(1, 5)
        ready = round(random.uniform(0, travel_hours), 1)
        due = round(travel_hours + random.uniform(3, 10), 1)  # generous slack so instances are usually feasible
        customers[i] = (demand, ready, due)

    distance = {}
    for i in coords:
        distance[i] = {}
        for j in coords:
            distance[i][j] = math.dist(coords[i], coords[j])

    return {
        "depot": 0,
        "capacity": capacity,
        "num_vehicles": num_vehicles,
        "customers": customers,
        "distance": distance,
        "city_ids": list(coords.keys()),
    }


def run_benchmark(sizes=(10, 20, 30, 40)):
    rows = []
    for n in sizes:
        problem = make_synthetic_instance(n)

        t0 = time.perf_counter()
        greedy_routes, unserved = greedy_construct(problem)
        t_greedy = time.perf_counter() - t0
        greedy_total = total_solution_distance(greedy_routes, problem)

        t0 = time.perf_counter()
        improved_routes = two_opt_improve(greedy_routes, problem)
        t_2opt = time.perf_counter() - t0
        improved_total = total_solution_distance(improved_routes, problem)

        pct_improvement = ((greedy_total - improved_total) / greedy_total * 100) if greedy_total else 0

        rows.append({
            "n_customers": n,
            "customers_unserved": len(unserved),
            "greedy_distance": greedy_total,
            "greedy_time_ms": t_greedy * 1000,
            "two_opt_distance": improved_total,
            "two_opt_time_ms": t_2opt * 1000,
            "pct_improvement": pct_improvement,
        })
    return rows


if __name__ == "__main__":
    results = run_benchmark()
    with open(os.path.join(_THIS_DIR, "results_vrptw_synthetic.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for r in results:
        print(f"\n--- n_customers = {r['n_customers']} (unserved: {r['customers_unserved']}) ---")
        print(f"  Greedy:  {r['greedy_distance']:.1f} units, {r['greedy_time_ms']:.3f}ms")
        print(f"  2-opt:   {r['two_opt_distance']:.1f} units, {r['two_opt_time_ms']:.3f}ms")
        print(f"  Improvement: {r['pct_improvement']:.1f}%")