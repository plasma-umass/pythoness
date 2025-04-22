import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from itertools import combinations
    
        def manhattan_dist(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
        def is_feasible(distance):
            selected = [False] * len(points)
            count = 0
            last = -1
            while count < k:
                found = False
                for i in range(len(points)):
                    if not selected[i] and (last == -1 or manhattan_dist(points[last], points[i]) >= distance):
                        selected[i] = True
                        last = i
                        count += 1
                        found = True
                        break
                if not found:
                    return False
            return True
        (left, right) = (0, 2 * side)
        max_min_distance = 0
        while left <= right:
            mid = (left + right) // 2
            if is_feasible(mid):
                max_min_distance = mid
                left = mid + 1
            else:
                right = mid - 1
        return max_min_distance