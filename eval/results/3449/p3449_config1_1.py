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
        # We need to compute the maximum possible minimum value after making m moves
        dp = [[-float('inf')] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0  # Starting point with index before the first point
        # Iterate over permissible moves
        for move in range(1, m + 1):
            for i in range(n + 1):
                if i > 0:  # Move right
                    dp[i][move] = max(dp[i][move], dp[i - 1][move - 1] + points[i - 1])
                if i < n:  # Move left
                    dp[i][move] = max(dp[i][move], dp[i + 1][move - 1] - points[i])
        # Get maximum of possible minimums in the dp table for exactly m moves
        max_min_value = max((dp[i][m] for i in range(n + 1)))
        return max_min_value