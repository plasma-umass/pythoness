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
    
        def sliding_window_minimum(arr, k):
            min_deque = deque()
            min_vals = []
            for (i, num) in enumerate(arr):
                while min_deque and arr[min_deque[-1]] > num:
                    min_deque.pop()
                min_deque.append(i)
                if min_deque[0] == i - k:
                    min_deque.popleft()
                if i >= k - 1:
                    min_vals.append(arr[min_deque[0]])
            return min_vals
    
        def sliding_window_maximum(arr, k):
            max_deque = deque()
            max_vals = []
            for (i, num) in enumerate(arr):
                while max_deque and arr[max_deque[-1]] < num:
                    max_deque.pop()
                max_deque.append(i)
                if max_deque[0] == i - k:
                    max_deque.popleft()
                if i >= k - 1:
                    max_vals.append(arr[max_deque[0]])
            return max_vals
        total_sum = 0
        n = len(nums)
        for subarray_size in range(1, k + 1):
            min_vals = sliding_window_minimum(nums, subarray_size)
            max_vals = sliding_window_maximum(nums, subarray_size)
            for i in range(n - subarray_size + 1):
                total_sum += min_vals[i] + max_vals[i]
        return str(total_sum)