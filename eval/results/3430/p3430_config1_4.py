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
    
        def sum_min_max_of_subarrays(size: int) -> int:
            min_deque = deque()  # Store indices of nums in increasing order of value
            max_deque = deque()  # Store indices of nums in decreasing order of value
            current_sum = 0
            for i in range(len(nums)):
                # Maintain the window to only store indices of current subarray element limits
                if min_deque and min_deque[0] < i - size + 1:
                    min_deque.popleft()
                if max_deque and max_deque[0] < i - size + 1:
                    max_deque.popleft()
                # Update deques with new element
                while min_deque and nums[min_deque[-1]] >= nums[i]:
                    min_deque.pop()
                while max_deque and nums[max_deque[-1]] <= nums[i]:
                    max_deque.pop()
                min_deque.append(i)
                max_deque.append(i)
                # Add min and max of the current window if window size is at least 'size'
                if i >= size - 1:
                    current_sum += nums[min_deque[0]] + nums[max_deque[0]]
            return current_sum
        total_sum = 0
        # Calculate the sum of min and max for all possible sizes from 1 to k
        for size in range(1, k + 1):
            total_sum += sum_min_max_of_subarrays(size)
        return total_sum