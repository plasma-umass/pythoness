import pythoness
from typing import List, Optional

def fullBloomFlowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    """
    You are given a 0-indexed 2D integer array flowers, where flowers[i] = [starti, endi] means the i^th flower will be in full bloom from starti to endi (inclusive). You are also given a 0-indexed integer array people of size n, where people[i] is the time that the i^th person will arrive to see the flowers.
    Return an integer array answer of size n, where answer[i] is the number of flowers that are in full bloom when the i^th person arrives.

    Constraints:

    1 <= flowers.length <= 5 * 10^4
    flowers[i].length == 2
    1 <= starti <= endi <= 10^9
    1 <= people.length <= 5 * 10^4
    1 <= people[i] <= 10^9
    """
    import bisect
    # Prepare lists of start and end times
    start_times = []
    end_times = []
    for (start, end) in flowers:
        start_times.append(start)
        end_times.append(end)
    # Sort the start and end times
    start_times.sort()
    end_times.sort()
    # For each person's arrival time, calculate number of flowers in bloom
    result = []
    for arrival in people:
        # Number of flowers that have started blooming by `arrival`
        started_blooming = bisect.bisect_right(start_times, arrival)
        # Number of flowers that have ended blooming before `arrival`
        ended_blooming = bisect.bisect_left(end_times, arrival)
        # Calculate flowers that are blooming at `arrival`
        result.append(started_blooming - ended_blooming)
    return result
fullBloomFlowers(flowers=[[1, 6], [3, 7], [9, 12], [4, 13]], people=[2, 3, 7, 11])