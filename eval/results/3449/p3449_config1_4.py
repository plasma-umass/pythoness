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
    
        def isPossible(min_val):
            deque_list = deque([0])
            cur_sum = 0
            length = len(points)
            for i in range(length):
                points[i] -= min_val
            for i in range(length):
                cur_sum += points[i]
                # Maintain the window of size m
                if i - deque_list[0] > m:
                    deque_list.popleft()
                # The maximum sum of m sized subarray should be non-negative
                if i >= m - 1 and cur_sum - points[deque_list[0]] >= 0:
                    return True
                while deque_list and cur_sum <= cur_sum - points[deque_list[-1]]:
                    deque_list.pop()
                deque_list.append(i + 1)
            return False
        (low, high) = (min(points), max(points))
        result = low
        while low <= high:
            mid = (low + high) // 2
            if isPossible(mid):
                result = mid
                low = mid + 1
            else:
                high = mid - 1
        return result