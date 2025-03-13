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
    from bisect import bisect_right, bisect_left
    # Separate and sort the start and end times of flowers
    start_times = sorted([start for (start, end) in flowers])
    end_times = sorted([end for (start, end) in flowers])
    answer = []
    for person in people:
        # Count how many flowers have started blooming (those with start time <= person)
        flowers_started = bisect_right(start_times, person)
        # Count how many flowers have finished blooming (those with end time < person)
        flowers_ended = bisect_left(end_times, person)
        # Current blooming flowers
        answer.append(flowers_started - flowers_ended)
    return answer
fullBloomFlowers(flowers=[[1, 6], [3, 7], [9, 12], [4, 13]], people=[2, 3, 7, 11])