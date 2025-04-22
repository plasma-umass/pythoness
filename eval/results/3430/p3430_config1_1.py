import pythoness
from typing import List, Optional

class Solution:
    
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of the maximum and minimum elements of all subarrays with at most k elements from an integer array nums.
    
        Constraints:
        1 <= nums.length <= 80000, 1 <= k <= nums.length, and -10^6 <= nums[i] <= 10^6.
        """
        from collections import deque
    
        def sumMinMax(arr):
            min_deque = deque()
            max_deque = deque()
            sum_min_max = 0
            for (i, num) in enumerate(arr):
                while min_deque and arr[min_deque[-1]] >= num:
                    min_deque.pop()
                min_deque.append(i)
                while max_deque and arr[max_deque[-1]] <= num:
                    max_deque.pop()
                max_deque.append(i)
                if i >= k and min_deque[0] == i - k:
                    min_deque.popleft()
                if i >= k and max_deque[0] == i - k:
                    max_deque.popleft()
                sum_min_max += arr[min_deque[0]] + arr[max_deque[0]]
            return sum_min_max
        total_sum = 0
        n = len(nums)
        for window_size in range(1, k + 1):
            total_sum += sumMinMax(nums[:window_size])
            for start in range(1, n - window_size + 1):
                total_sum += sumMinMax(nums[start:start + window_size])
        return total_sum