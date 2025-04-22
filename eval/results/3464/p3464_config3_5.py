import pythoness
from typing import List, Optional

class Solution:
    
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array
        points of coordinates on the boundary of the square, this function selects k elements from points to maximize the
        minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the
        absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance
        for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.
        """
        from itertools import combinations
    
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        # Generate all combinations of points taking k at a time
        all_combinations = combinations(points, k)
        # Initialize the maximum of minimum distances
        max_of_min_distances = 0
        for selected_points in all_combinations:
            # For each combination, calculate distances between each pair
            min_distance = float('inf')
            for i in range(k):
                for j in range(i + 1, k):
                    dist = manhattan_distance(selected_points[i], selected_points[j])
                    min_distance = min(min_distance, dist)
            # Update the maximum of the minimum distances found
            max_of_min_distances = max(max_of_min_distances, min_distance)
        return max_of_min_distances