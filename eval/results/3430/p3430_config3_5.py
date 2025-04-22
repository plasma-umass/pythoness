import pythoness
from typing import List, Optional

class Solution:
    
    def minMaxSubarraySum(self, nums, k):
        """
        Calculate the sum of the maximum and minimum elements of all subarrays with at most k elements from an integer array nums.
    
        Constraints:
        1 <= nums.length <= 80000, 1 <= k <= nums.length, and -10^6 <= nums[i] <= 10^6.
        """
        from collections import deque
        n = len(nums)
        total_sum = 0
        for l in range(1, k + 1):
            min_queue = deque()
            max_queue = deque()
            subarray_sum = 0
            for i in range(n):
                # Maintain the min queue
                while min_queue and nums[min_queue[-1]] >= nums[i]:
                    min_queue.pop()
                min_queue.append(i)
                # Maintain the max queue
                while max_queue and nums[max_queue[-1]] <= nums[i]:
                    max_queue.pop()
                max_queue.append(i)
                # Remove elements not within the window
                if min_queue[0] < i - l + 1:
                    min_queue.popleft()
                if max_queue[0] < i - l + 1:
                    max_queue.popleft()
                if i >= l - 1:
                    min_val = nums[min_queue[0]]
                    max_val = nums[max_queue[0]]
                    subarray_sum += min_val + max_val
            total_sum += subarray_sum
        return str(total_sum)