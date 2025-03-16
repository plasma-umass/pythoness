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
    """

    def canPlacePointsWithDist(d: int) -> bool:
        # Helper function to determine if it is possible to choose k points
        # such that each point has at least distance d from each other
        placed_points = []
        for point in points:
            if all((abs(point[0] - other[0]) + abs(point[1] - other[1]) >= d for other in placed_points)):
                placed_points.append(point)
                if len(placed_points) == k:
                    return True
        return False
    # Binary search to find the maximum minimum distance
    (left, right) = (0, 2 * side)
    while left < right:
        mid = (left + right + 1) // 2
        if canPlacePointsWithDist(mid):
            left = mid
        else:
            right = mid - 1
    return left
maxDistance(side=2, points=[[0, 2], [2, 0], [2, 2], [0, 0]], k=4)