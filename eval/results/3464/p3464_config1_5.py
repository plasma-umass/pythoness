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
    
        def is_valid_distance(min_distance):
            """
            Check if it's possible to select k points such that the minimum distance 
            between any pair of points is at least min_distance.
            """
            # Try to select points greedily, maintaining the current selection.
            selected_points = [points[0]]
            for point in points[1:]:
                if all((manhattan_distance(point, selected) >= min_distance for selected in selected_points)):
                    selected_points.append(point)
                if len(selected_points) == k:
                    return True
            return len(selected_points) == k
        # Sorting the points could allow us to try combinations such that selected
        # points will maintain the threshold with this sequence.
        points.sort()
        # Binary search over the possible minimum distance from 0 to 2 * side.
        (low, high) = (0, 2 * side)
        best_min_distance = 0
        while low <= high:
            mid = (low + high) // 2
            if is_valid_distance(mid):
                best_min_distance = mid
                low = mid + 1
            else:
                high = mid - 1
        return best_min_distance