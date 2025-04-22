import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from itertools import combinations
        from math import inf
    
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
        def is_valid_distance(d):
            """
            Check if it's possible to select k points such that
            the minimum Manhattan distance between any two of them is at least d.
            """
            selected = [points[0]]
            for _ in range(1, k):
                next_point = None
                for p in points:
                    if all((manhattan_distance(p, sp) >= d for sp in selected)):
                        next_point = p
                        break
                if next_point is None:
                    return False
                selected.append(next_point)
            return True
        points.sort()
        (low, high) = (0, side * 2)
        best_dist = 0
        while low <= high:
            mid = (low + high) // 2
            if is_valid_distance(mid):
                best_dist = mid
                low = mid + 1
            else:
                high = mid - 1
        return best_dist