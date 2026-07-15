"""
Weighted Job Scheduling - DP problem for task 3.

Framing it as delivery trip scheduling: a single driver/vehicle has a
list of possible delivery jobs, each with a start time, end time, and
profit. Jobs can't overlap (one driver can't do two trips at once), so
the goal is picking a subset of non-overlapping jobs that maximises
total profit.

Recurrence:
    Sort jobs by end time first.
    For job i (1-indexed after sorting), let p(i) = the largest index j
    such that job j's end time <= job i's start time (last job that
    doesn't conflict with i). Found with binary search since the jobs
    are sorted by end time.

    dp[i] = max(
        dp[i-1],                  # skip job i
        profit[i] + dp[p(i)]      # take job i, add best from non-conflicting jobs before it
    )

    dp[0] = 0 (base case, no jobs -> 0 profit)

Answer is dp[n]. Table is filled bottom-up left to right since dp[i]
only depends on smaller indices - no need for recursion/memoisation,
though a top-down memoised version would compute the exact same values,
just in a different order (and with recursion overhead on top).
"""
import bisect


def schedule_jobs(jobs):
    """
    jobs: list of (start, end, profit) tuples.
    returns (max_profit, selected_jobs)
    """
    if not jobs:
        return 0, []

    # sort by end time - this is what makes the binary search for p(i) work
    jobs_sorted = sorted(jobs, key=lambda j: j[1])
    n = len(jobs_sorted)
    ends = [j[1] for j in jobs_sorted]

    dp = [0] * (n + 1)          # dp[i] = best profit using first i jobs (sorted)
    take = [False] * (n + 1)    # did we take job i in the optimal solution up to i

    for i in range(1, n + 1):
        start_i, end_i, profit_i = jobs_sorted[i - 1]

        # p(i): latest job (0-indexed in jobs_sorted) whose end <= start_i
        # bisect_right on ends gives us the insertion point, which is
        # exactly the count of jobs that end at or before start_i
        p = bisect.bisect_right(ends, start_i)

        include_profit = profit_i + dp[p]
        exclude_profit = dp[i - 1]

        if include_profit > exclude_profit:
            dp[i] = include_profit
            take[i] = True
        else:
            dp[i] = exclude_profit
            take[i] = False

    # walk back through `take` to figure out which jobs actually got picked
    selected = []
    i = n
    while i > 0:
        if take[i]:
            selected.append(jobs_sorted[i - 1])
            start_i = jobs_sorted[i - 1][0]
            i = bisect.bisect_right(ends, start_i)
        else:
            i -= 1
    selected.reverse()

    return dp[n], selected


def brute_force_schedule(jobs):
    """
    O(2^n) brute force - tries every subset, keeps the best valid
    (non-overlapping) one. Only here to sanity-check the DP answer on
    small inputs, not meant to actually run on large job lists.
    """
    from itertools import combinations

    best_profit = 0
    best_subset = []
    n = len(jobs)
    for r in range(n + 1):
        for subset in combinations(jobs, r):
            sorted_subset = sorted(subset, key=lambda j: j[1])
            valid = True
            for k in range(1, len(sorted_subset)):
                if sorted_subset[k][0] < sorted_subset[k - 1][1]:
                    valid = False
                    break
            if valid:
                profit = sum(j[2] for j in subset)
                if profit > best_profit:
                    best_profit = profit
                    best_subset = sorted_subset
    return best_profit, best_subset


if __name__ == "__main__":
    # sample delivery jobs: (start_hour, end_hour, profit_npr)
    sample_jobs = [
        (1, 3, 500), (2, 5, 800), (4, 6, 400), (6, 9, 900),
        (5, 8, 750), (8, 10, 300), (3, 7, 1000),
    ]
    profit, selected = schedule_jobs(sample_jobs)
    print("DP result - max profit:", profit)
    print("Selected jobs:", selected)

    bf_profit, bf_selected = brute_force_schedule(sample_jobs)
    print("Brute force result - max profit:", bf_profit)
    assert profit == bf_profit, "DP and brute force disagree - bug somewhere"
    print("DP matches brute force, looks correct")