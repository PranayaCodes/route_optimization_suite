"""
Greedy construction heuristic for VRPTW - heuristic #1 of 2 required by
the brief.

Idea: start a vehicle at the depot. Repeatedly look at all not-yet-served
customers, and pick whichever one is closest to the vehicle's current
position AND can still be reached without breaking capacity or its time
window. Add it to the route, move the vehicle there, repeat. The moment
no remaining customer is feasible to add next, close this route (send
the vehicle back to the depot) and start a fresh vehicle for whatever's
left.

This is the "problem-specific construction heuristic" the brief asks
for - fast (no backtracking, no search), but obviously not guaranteed
optimal since it only ever looks one step ahead.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vrptw_problem import get_problem, route_is_feasible, route_distance, total_solution_distance, SPEED_KMH


def greedy_construct(problem):
    unserved = set(problem["customers"].keys())
    routes = []

    while unserved and len(routes) < problem["num_vehicles"]:
        route = []
        load = 0
        time = 0.0
        position = problem["depot"]

        while True:
            best_candidate = None
            best_dist = float("inf")

            for c in unserved:
                demand, ready, due = problem["customers"][c]
                if load + demand > problem["capacity"]:
                    continue  # would overload the truck, skip

                dist = problem["distance"][position][c]
                travel_hours = dist / SPEED_KMH
                arrival = time + travel_hours
                if arrival > due:
                    continue  # would arrive too late, skip

                if dist < best_dist:
                    best_dist = dist
                    best_candidate = c

            if best_candidate is None:
                break  # nothing left fits on this route, close it out

            demand, ready, due = problem["customers"][best_candidate]
            arrival = time + (best_dist / SPEED_KMH)
            time = max(arrival, ready)  # wait if we arrived before the window opened
            load += demand
            position = best_candidate
            route.append(best_candidate)
            unserved.remove(best_candidate)

        if route:
            routes.append(route)
        else:
            break  # a vehicle found literally nothing feasible, no point looping further

    return routes, unserved  # unserved is non-empty if we ran out of vehicles


if __name__ == "__main__":
    problem = get_problem()
    routes, unserved = greedy_construct(problem)

    print(f"Vehicles used: {len(routes)} / {problem['num_vehicles']}")
    for i, route in enumerate(routes):
        feasible, msg = route_is_feasible(route, problem)
        dist = route_distance(route, problem)
        print(f"  Vehicle {i+1}: {route} -- {dist:.1f}km -- feasible: {feasible}")

    if unserved:
        print(f"WARNING: {len(unserved)} customers not served: {unserved}")
    else:
        print("All customers served.")

    print(f"Total distance: {total_solution_distance(routes, problem):.1f}km")