import pythoness
from typing import List, Optional

def maxDistance(side: int, points: List[List[int]], k: int) -> int:
    """
    You are given an integer side, representing the edge length of a square with corners at (0, 0), (0, side), (side, 0), and (side, side) on a Cartesian plane.
    You are also given a positive integer k and a 2D integer array points, where points[i] = [xi, yi] represents the coordinate of a point lying on the boundary of the square.
    You need to select k elements among points such that the minimum Manhattan distance between any two points is maximized.
    Return the maximum possible minimum Manhattan distance between the selected k points.
    The Manhattan Distance between two cells (xi, yi) and (xj, yj) is |xi - xj| + |yi - yj|.

    Constraints:

    1 <= side <= 10^9
    4 <= points.length <= min(4 * side, 15 * 10^3)
    points[i] == [xi, yi]
    The input is generated such that:

    points[i] lies on the boundary of the square.
    All points[i] are unique.

    4 <= k <= min(25, points.length)

    """
    from typing import List

    def canPlace(points, mid, k):
        placed = [points[0]]
        for p in points[1:]:
            if all((abs(p[0] - q[0]) + abs(p[1] - q[1]) >= mid for q in placed)):
                placed.append(p)
                if len(placed) >= k:
                    return True
        return len(placed) >= k
    points.sort()
    (low, high) = (0, 2 * side)
    result = 0
    while low <= high:
        mid = (low + high) // 2
        if canPlace(points, mid, k):
            result = mid
            low = mid + 1
        else:
            high = mid - 1
    return result
maxDistance(side=2, points=[[0, 2], [2, 0], [2, 2], [0, 0]], k=4)