import pythoness
from typing import List, Optional

class Solution:
    
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Calculate the maximum possible minimum value in an array gameScore, after making at most m moves within 
        a bounds-constrained index system starting from before the first index. In each move, the index can 
        increase or decrease by 1, and the corresponding points are added to gameScore at that index.
        """
        n = len(points)
        prefix_sum = [0] * (n + 1)
        # Calculate prefix sums
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + points[i]
        # Helper function to get the sum from index i to j
    
        def get_sum(i, j):
            return prefix_sum[j + 1] - prefix_sum[i]
        # Initialize variables
        max_min_score = float('-inf')
        # Loop over all possible start indices
        for start in range(min(n, m + 1)):
            # Minimum score from starting index
            min_score = float('inf')
            # Loop over all possible end indices from this start point
            for end in range(start, min(n, start + m + 1)):
                # Calculate range sum
                current_sum = get_sum(start, end)
                # Update minimum score found in this subarray
                min_score = min(min_score, current_sum)
            # Update maximum of all minimum scores
            max_min_score = max(max_min_score, min_score)
        return max_min_score