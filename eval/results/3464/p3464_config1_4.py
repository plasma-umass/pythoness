import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from itertools import combinations
    
        def manhattan_distance(point1, point2):
            return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
    
        def is_feasible(d):
            selected_points = 0
            last_selected = (-1, -1)
            for i in range(len(sorted_points)):
                if last_selected == (-1, -1) or manhattan_distance(sorted_points[i], last_selected) >= d:
                    selected_points += 1
                    last_selected = sorted_points[i]
                    if selected_points == k:
                        return True
            return False
        sorted_points = sorted(points)
        (left, right) = (0, 2 * side)
        result = 0
        while left <= right:
            mid = (left + right) // 2
            if is_feasible(mid):
                result = mid
                left = mid + 1
            else:
                right = mid - 1
        return result