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
    
        def sum_of_min_max_subarrays(nums, k):
            n = len(nums)
            min_sum = 0
            max_sum = 0
            min_deque = deque()
            max_deque = deque()
            for i in range(n):
                while min_deque and min_deque[0] <= i - k:
                    min_deque.popleft()
                while max_deque and max_deque[0] <= i - k:
                    max_deque.popleft()
                while min_deque and nums[min_deque[-1]] >= nums[i]:
                    min_deque.pop()
                while max_deque and nums[max_deque[-1]] <= nums[i]:
                    max_deque.pop()
                min_deque.append(i)
                max_deque.append(i)
                if i >= k - 1:
                    min_sum += nums[min_deque[0]]
                    max_sum += nums[max_deque[0]]
            return min_sum + max_sum
        result = 0
        for window_size in range(1, k + 1):
            result += sum_of_min_max_subarrays(nums, window_size)
        return str(result)