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
        n = len(points)
        gameScore = [[-float('inf')] * (m + 1) for _ in range(n + 1)]
        gameScore[0][0] = 0
        for moves in range(m):
            for index in range(n):
                if gameScore[index][moves] == -float('inf'):
                    continue
                if index + 1 < n:
                    gameScore[index + 1][moves + 1] = max(gameScore[index + 1][moves + 1], gameScore[index][moves] + points[index + 1])
                if index - 1 >= 0:
                    gameScore[index - 1][moves + 1] = max(gameScore[index - 1][moves + 1], gameScore[index][moves] + points[index - 1])
        return max((gameScore[index][m] for index in range(n)))