import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from typing import List
        # Helper function to calculate Manhattan distance
    
        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        # Binary search over the possible minimum distances
    
        def canAchieveMinDistance(d):
            # Try to pick k points such that all pairwise distances are at least d
            # A greedy or backtracking approach to check feasibility
    
            def helper(selected):
                if len(selected) == k:
                    return True
                for point in points:
                    if all((manhattan(point, sp) >= d for sp in selected)):
                        selected.append(point)
                        if helper(selected):
                            return True
                        selected.pop()
                return False
            return helper([])
        # Initialize binary search bounds
        (low, high) = (0, side * 2)
        result = 0
        while low <= high:
            mid = (low + high) // 2
            if canAchieveMinDistance(mid):
                result = mid
                low = mid + 1
            else:
                high = mid - 1
        return result