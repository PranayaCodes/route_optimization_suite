"""
Vehicle Routing Problem with Time Windows - problem setup for task 4.

Depot is Kathmandu (city 0). Customers are the other 11 cities in the
Nepal network, each needing a delivery with:
  - demand: how much cargo space it takes up on the truck
  - time window (ready, due): the delivery has to arrive within this
    window, in hours from the start of the day

A fleet of vehicles, each with limited capacity, starts and ends at the
depot. Travel time between cities is just distance in km treated as
hours (i.e. assuming an average speed of 1km per "time unit" - unrealistic
as an actual speed but keeps the numbers simple and doesn't change
anything about how the algorithms work).

Why this is NP-Hard: VRPTW is a generalisation of the Travelling
Salesman Problem - if you set the number of vehicles to 1, remove the
capacity limit, and set every time window to [0, infinity], a VRPTW
instance becomes exactly a TSP instance (find the shortest single route
visiting every customer). Since TSP is NP-Hard, and TSP instances can be
expressed as VRPTW instances without doing any extra work, VRPTW can't
be easier than TSP - it's NP-Hard too (and arguably harder in practice,
since it also has to respect capacity and timing constraints on top of
finding a short route).
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task2_graph_algorithms"))

from nepal_network import CITY_NAMES
from distance_matrix import build_distance_matrix

DEPOT = 0
VEHICLE_CAPACITY = 12
NUM_VEHICLES = 4
SPEED_KMH = 50  # rough average highway speed, used only to convert km -> hours for time windows

# customer_id: (demand, ready_time_hours, due_time_hours)
# windows are set relative to actual one-way travel time from the depot
# (see distances printed by distance_matrix.py) - e.g. Dhangadhi is
# ~746km from Kathmandu, which is ~15 hours at 50km/h, so its window
# has to be late enough to actually be reachable
CUSTOMERS = {
    1:  (3, 0, 8),     # Pokhara      (~4h direct)
    2:  (2, 0, 3),     # Lalitpur     (~0.1h direct, close + tight window)
    3:  (2, 0, 3),     # Bhaktapur    (~0.3h direct, close + tight window)
    4:  (4, 8, 20),    # Biratnagar   (~10h direct, needs a late window)
    5:  (3, 2, 10),    # Birgunj      (~4.5h direct)
    7:  (3, 0, 6),     # Bharatpur    (~3h direct)
    8:  (4, 2, 12),    # Butwal       (~5.3h direct)
    9:  (5, 10, 20),   # Dhangadhi    (~15h direct - furthest city, needs the latest window)
    10: (2, 4, 14),    # Janakpur     (~6.3h direct)
    11: (2, 0, 6),     # Hetauda      (~2.7h direct)
    12: (4, 8, 20),    # Nepalgunj    (~10.6h direct)
}


def get_problem():
    matrix, city_ids = build_distance_matrix()
    return {
        "depot": DEPOT,
        "capacity": VEHICLE_CAPACITY,
        "num_vehicles": NUM_VEHICLES,
        "customers": CUSTOMERS,
        "distance": matrix,
        "city_ids": city_ids,
    }


def route_is_feasible(route, problem):
    """
    route: list of customer ids in visiting order (depot not included).
    Checks capacity and that every customer is reached within its time
    window, given the vehicle leaves the depot at time 0. Travel time
    between cities i and j is distance[i][j] / SPEED_KMH (converting km
    to hours) - NOT raw km, since the time windows are in hours.
    """
    demand_total = sum(problem["customers"][c][0] for c in route)
    if demand_total > problem["capacity"]:
        return False, "over capacity"

    time = 0.0
    prev = problem["depot"]
    for c in route:
        travel_hours = problem["distance"][prev][c] / SPEED_KMH
        arrival = time + travel_hours
        ready, due = problem["customers"][c][1], problem["customers"][c][2]
        if arrival > due:
            return False, f"misses time window at city {c} (arrive {arrival:.1f}h, due {due}h)"
        # if we arrive early, we just wait until the window opens
        time = max(arrival, ready)
        prev = c
    return True, "ok"


def route_distance(route, problem):
    """Total distance for a route, depot -> customers -> back to depot."""
    if not route:
        return 0
    total = problem["distance"][problem["depot"]][route[0]]
    for i in range(len(route) - 1):
        total += problem["distance"][route[i]][route[i + 1]]
    total += problem["distance"][route[-1]][problem["depot"]]
    return total


def total_solution_distance(routes, problem):
    return sum(route_distance(r, problem) for r in routes)


if __name__ == "__main__":
    problem = get_problem()
    print(f"Depot: {CITY_NAMES[problem['depot']]}")
    print(f"Vehicle capacity: {problem['capacity']}, vehicles available: {problem['num_vehicles']}")
    print(f"Customers: {len(problem['customers'])}, total demand: {sum(c[0] for c in problem['customers'].values())}")
    print(f"Min vehicles needed just on capacity: "
          f"{-(-sum(c[0] for c in problem['customers'].values()) // problem['capacity'])}")  # ceiling division