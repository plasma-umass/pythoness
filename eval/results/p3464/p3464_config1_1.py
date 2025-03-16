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

    def manhattan_dist(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def can_form_k_points_with_min_dist(d):

        def place_points(i, k_left):
            if k_left == 0:
                return True
            if i >= len(points):
                return False
            # Attempt to place this point
            selected.append(i)
            if all((manhattan_dist(points[i], points[j]) >= d for j in selected[:-1])):
                if place_points(i + 1, k_left - 1):
                    return True
            # Backtrack
            selected.pop()
            return place_points(i + 1, k_left)
        selected = []
        return place_points(0, k)
    points.sort()
    (left, right) = (0, 2 * side)
    result = 0
    while left <= right:
        mid = (left + right) // 2
        if can_form_k_points_with_min_dist(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result
maxDistance(side=2, points=[[0, 2], [2, 0], [2, 2], [0, 0]], k=4)