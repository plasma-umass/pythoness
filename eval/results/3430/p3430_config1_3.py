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
    
        def sum_of_min_max_elements(subarrays) -> int:
            total = 0
            for subarray in subarrays:
                if subarray:
                    total += min(subarray) + max(subarray)
            return total
        n = len(nums)
        min_queue = deque()  # deque to store indices of the minimum values
        max_queue = deque()  # deque to store indices of the maximum values
        subarray_indices = []
        # Iterate over all subarray sizes up to k
        for size in range(1, k + 1):
            # Reset deque for new subarray size
            min_queue.clear()
            max_queue.clear()
            # Process first 'size' elements
            for i in range(size):
                while min_queue and nums[min_queue[-1]] >= nums[i]:
                    min_queue.pop()
                while max_queue and nums[max_queue[-1]] <= nums[i]:
                    max_queue.pop()
                min_queue.append(i)
                max_queue.append(i)
            # Collect indices for subarray
            subarray_indices.append((min_queue[0], max_queue[0]))
            # Process the rest of the elements
            for i in range(size, n):
                # Remove elements not within the current subarray window
                while min_queue and min_queue[0] <= i - size:
                    min_queue.popleft()
                while max_queue and max_queue[0] <= i - size:
                    max_queue.popleft()
                # Add new element
                while min_queue and nums[min_queue[-1]] >= nums[i]:
                    min_queue.pop()
                while max_queue and nums[max_queue[-1]] <= nums[i]:
                    max_queue.pop()
                min_queue.append(i)
                max_queue.append(i)
                # Collect indices for subarray
                subarray_indices.append((min_queue[0], max_queue[0]))
        # Create all subarrays and calculate the sum of min and max
        subarrays = [nums[i:j + 1] for (i, j) in subarray_indices]
        return sum_of_min_max_elements(subarrays)