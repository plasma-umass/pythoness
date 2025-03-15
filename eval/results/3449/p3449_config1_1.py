import pythoness
from typing import List, Optional
import heapq
from typing import List

def maxScore(points: List[int], m: int) -> int:
    """
    You are given an array points of size n and an integer m. There is another array gameScore of size n, where gameScore[i] represents the score achieved at the i^th game. Initially, gameScore[i] == 0 for all i.
    You start at index -1, which is outside the array (before the first position at index 0). You can make at most m moves. In each move, you can either:

    Increase the index by 1 and add points[i] to gameScore[i].
    Decrease the index by 1 and add points[i] to gameScore[i].

    Note that the index must always remain within the bounds of the array after the first move.
    Return the maximum possible minimum value in gameScore after at most m moves.

    Constraints:
    2 <= n == points.length <= 5 * 10^4
    1 <= points[i] <= 10^6
    1 <= m <= 10^9

    """
    n = len(points)
    left_moves = right_moves = m
    max_min = 0
    # Priority queue to track the smallest values at each position
    pq = [0] * n
    for i in range(n):
        if i <= left_moves:
            pq[i] = points[i]
        else:
            pq[i] = points[i] + min(pq[i - 1], pq[i - left_moves - 1])
    # Initially, try using right_moves
    max_min = max(max_min, min(pq))  # pq is counting as deque from right
    # Overall loop from right
    for j in range(n - 1, -1, -1):
        if j < n - right_moves - 1:
            break
        right_index = max(0, j - right_moves)
        pq[j] = points[j]
        if j < n - 1:
            pq[j] += min(pq[j + 1], pq[j])
    max_min = max(max_min, min(pq))
    return max_min
maxScore(points=[2, 4], m=3)