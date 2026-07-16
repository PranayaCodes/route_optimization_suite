"""
2-opt local search - heuristic #2 of 2 required by the brief.

Takes whatever solution greedy_construction.py builds and tries to
improve it: for each route, look at every pair of positions, reverse
the segment between them, and keep the reversal if it's both still
feasible (capacity/time windows) AND shorter than before. Keep sweeping
over all routes until a full pass finds no improving swap.

This is a standard TSP-style 2-opt move applied per-route (each VRPTW
route is basically its own little TSP once the customer set for that
vehicle is fixed) - it can't move customers between vehicles or change
who's on which route, it just improves the order within each route.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vrptw_problem import get_problem, route_is_feasible, route_distance, total_solution_distance
from greedy_construction import greedy_construct


def two_opt_route(route, problem):
    """Repeatedly apply the best improving 2-opt swap until none is left."""
    best_route = route[:]
    best_dist = route_distance(best_route, problem)
    improved = True

    while improved:
        improved = False
        n = len(best_route)
        for i in range(n - 1):
            for j in range(i + 1, n):
                candidate = best_route[:i] + best_route[i:j + 1][::-1] + best_route[j + 1:]
                feasible, _ = route_is_feasible(candidate, problem)
                if not feasible:
                    continue
                candidate_dist = route_distance(candidate, problem)
                if candidate_dist < best_dist:
                    best_route = candidate
                    best_dist = candidate_dist
                    improved = True
        # loop again from scratch if anything improved this pass
    return best_route


def two_opt_improve(routes, problem):
    return [two_opt_route(r, problem) for r in routes]


if __name__ == "__main__":
    problem = get_problem()
    greedy_routes, unserved = greedy_construct(problem)
    greedy_total = total_solution_distance(greedy_routes, problem)

    improved_routes = two_opt_improve(greedy_routes, problem)
    improved_total = total_solution_distance(improved_routes, problem)

    print("--- Before 2-opt (greedy construction) ---")
    for i, r in enumerate(greedy_routes):
        print(f"  Vehicle {i+1}: {r} -- {route_distance(r, problem):.1f}km")
    print(f"  Total: {greedy_total:.1f}km")

    print("\n--- After 2-opt local search ---")
    for i, r in enumerate(improved_routes):
        print(f"  Vehicle {i+1}: {r} -- {route_distance(r, problem):.1f}km")
    print(f"  Total: {improved_total:.1f}km")

    saved = greedy_total - improved_total
    pct = (saved / greedy_total * 100) if greedy_total else 0
    print(f"\nImprovement: {saved:.1f}km saved ({pct:.1f}%)")