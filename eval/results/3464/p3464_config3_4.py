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
        # Binary search to maximize the minimum distance
    
        def is_valid(min_dist):
            # Use combinations to check if we can pick k points such that all pairwise distances are at least min_dist
            for selected_points in combinations(points, k):
                if all((manhattan_distance(p1, p2) >= min_dist for (p1, p2) in combinations(selected_points, 2))):
                    return True
            return False
        (left, right) = (0, side * 2)  # Maximum possible Manhattan distance on the boundary
        answer = 0
        while left <= right:
            mid = (left + right) // 2
            if is_valid(mid):
                answer = mid
                left = mid + 1
            else:
                right = mid - 1
        return answer