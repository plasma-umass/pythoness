import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array
        points of coordinates on the boundary of the square, this function selects k elements from points to maximize
        the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of
        the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum
        distance for the selected k points, considering constraints on the number of points and their uniqueness on the
        boundary.
        """
        from itertools import combinations
    
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
        def is_possible(min_dist):
            # Test if it's possible to choose k points with at least `min_dist` distance between them
            for combination in combinations(points, k):
                if all((manhattan_distance(combination[i], combination[j]) >= min_dist for i in range(k) for j in range(i + 1, k))):
                    return True
            return False
        (low, high) = (0, 2 * side)
        best = 0
        while low <= high:
            mid = (low + high) // 2
            if is_possible(mid):
                best = mid
                low = mid + 1
            else:
                high = mid - 1
        return best