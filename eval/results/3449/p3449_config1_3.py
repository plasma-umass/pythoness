import pythoness
from typing import List, Optional

class Solution:
    
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Calculate the maximum possible minimum value in an array gameScore, after making at most m moves within 
        a bounds-constrained index system starting from before the first index. In each move, the index can 
        increase or decrease by 1, and the corresponding points are added to gameScore at that index.
        """
        from collections import deque
        import sys
        n = len(points)
        # Initialize dp array where dp[i][j] represents the maximum possible score at index i with j moves.
        dp = [[-sys.maxsize] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for j in range(1, m + 1):
            for i in range(n):
                if i - 1 >= 0:
                    dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + points[i])
                if i + 1 < n:
                    dp[i][j] = max(dp[i][j], dp[i + 1][j - 1] + points[i])
        # Find the maximum minimum score
        max_min_score = -sys.maxsize
        for i in range(n):
            for j in range(m + 1):
                max_min_score = max(max_min_score, dp[i][j])
        return max_min_score