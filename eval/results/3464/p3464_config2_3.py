import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from itertools import combinations
    
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
        def is_valid(min_dist, points, k):
            # Check if it's possible to select k points with at least `min_dist` distance apart
            selected = []
            for point in points:
                if all((manhattan_distance(point, sel) >= min_dist for sel in selected)):
                    selected.append(point)
                    if len(selected) == k:
                        return True
            return False
        # Binary search for the largest minimum distance
        points.sort()  # sort the points for consistent combinations
        (low, high) = (0, side * 2)  # max distance on a square boundary
        while low < high:
            mid = (high - low + 1) // 2 + low
            # Mid is the current distance to validate
            if is_valid(mid, points, k):
                low = mid  # try for larger minimum distance
            else:
                high = mid - 1
        return low