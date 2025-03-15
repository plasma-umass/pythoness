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
    start_times = sorted((flower[0] for flower in flowers))
    end_times = sorted((flower[1] for flower in flowers))
    result = []
    for person in people:
        # Find the number of flowers that have started blooming by the time person arrives
        blooms_started = bisect_right(start_times, person)
        # Find the number of flowers that have stopped blooming by the time person arrives
        blooms_ended = bisect_left(end_times, person)
        # The number of flowers in full bloom when the person arrives
        full_bloom_count = blooms_started - blooms_ended
        result.append(full_bloom_count)
    return result
fullBloomFlowers(flowers=[[1, 6], [3, 7], [9, 12], [4, 13]], people=[2, 3, 7, 11])