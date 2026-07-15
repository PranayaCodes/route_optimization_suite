"""
Minimum Number of Platforms - greedy problem for task 3.

Framing: a bus/train station in the transportation network needs enough
platforms so that every scheduled arrival can actually dock, given some
trains/buses are at the station at the same time as others.

Greedy idea: sort all arrival times and all departure times separately.
Walk through both sorted lists together (two-pointer, like a merge
step) - every time we hit an arrival, one more platform is needed right
now; every time we hit a departure (that happens before or at the same
time as the next arrival), one platform frees up. Track the running
count and its max over the whole sweep - that max is the answer.

This is the "obviously correct" kind of greedy - the reasoning is just
that a platform is only needed for however long trains are physically
overlapping at the station, and sorting + sweeping is exactly measuring
peak overlap.
"""


def min_platforms(arrivals, departures):
    """
    arrivals, departures: lists of times (same length, arrivals[i]
    pairs with departures[i] for the same train). Returns
    (min_platforms_needed, timeline) where timeline is a list of
    (time, platforms_in_use) snapshots, for the visualisation.
    """
    n = len(arrivals)
    arr_sorted = sorted(arrivals)
    dep_sorted = sorted(departures)

    platforms_needed = 0
    max_platforms = 0
    i, j = 0, 0
    timeline = []

    while i < n and j < n:
        if arr_sorted[i] <= dep_sorted[j]:
            platforms_needed += 1
            max_platforms = max(max_platforms, platforms_needed)
            timeline.append((arr_sorted[i], platforms_needed))
            i += 1
        else:
            platforms_needed -= 1
            timeline.append((dep_sorted[j], platforms_needed))
            j += 1

    return max_platforms, timeline


def min_platforms_brute_force(arrivals, departures):
    """
    O(n^2) exact check - for every train's arrival time, count how many
    other trains are still at the station at that exact moment. The max
    of that count over all arrivals is the answer. Used just to confirm
    the greedy answer is actually correct, not because this is a good
    way to solve it for real.
    """
    n = len(arrivals)
    max_overlap = 0
    for i in range(n):
        overlap = 0
        for k in range(n):
            if arrivals[k] <= arrivals[i] <= departures[k]:
                overlap += 1
        max_overlap = max(max_overlap, overlap)
    return max_overlap


if __name__ == "__main__":
    # sample bus schedule at a station: arrival/departure hour (24h clock, as floats for simplicity)
    arrivals =   [9.0, 9.4, 9.5, 11.0, 15.0, 18.0]
    departures = [9.2, 12.0, 9.8, 11.2, 19.0, 20.0]

    result, timeline = min_platforms(arrivals, departures)
    print("Greedy result - platforms needed:", result)

    bf_result = min_platforms_brute_force(arrivals, departures)
    print("Brute force result - platforms needed:", bf_result)
    assert result == bf_result, "greedy and brute force disagree - bug somewhere"
    print("Greedy matches brute force, looks correct")
    print("Timeline (time, platforms in use):", timeline)