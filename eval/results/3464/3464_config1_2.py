import pythoness
from typing import List, Optional
from typing import List

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

    The function should pass the following tests:
        maxDistance(side = 2, points = [[0,2],[2,0],[2,2],[0,0]], k = 4) == 2
        maxDistance(side = 2, points = [[0,0],[1,2],[2,0],[2,2],[2,1]], k = 4) == 1
        maxDistance(side = 2, points = [[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]], k = 5) == 1
    """

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def canAchieveDistance(d):
        # Check if we can select k points such that the minimum Manhattan distance between
        # any two selected points is at least d
        # This uses a greedy algorithm to attempt selecting points
        selected = []
        for point in points:
            if len(selected) == 0:
                selected.append(point)
            elif all((manhattan_distance(point, sel) >= d for sel in selected)):
                selected.append(point)
                if len(selected) == k:
                    return True
        return len(selected) >= k
    # Binary search to find the maximum minimum distance
    (low, high) = (0, 2 * side)
    best_distance = 0
    while low <= high:
        mid = (low + high) // 2
        if canAchieveDistance(mid):
            best_distance = mid
            low = mid + 1
        else:
            high = mid - 1
    return best_distance
maxDistance(side=2, points=[[0, 2], [2, 0], [2, 2], [0, 0]], k=4)