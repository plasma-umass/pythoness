import pythoness
from typing import List, Optional

class Solution:
    
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of the maximum and minimum elements of
        all subarrays with at most k elements from an integer array nums.
    
        Constraints:
        1 <= nums.length <= 80000, 1 <= k <= nums.length, and -10^6 <= nums[i] <= 10^6.
        """
        from collections import deque
    
        def sum_of_deques(deq_min, deq_max, start, end):
            total_sum = 0
            while deq_min and deq_min[0] < start:
                deq_min.popleft()
            while deq_max and deq_max[0] < start:
                deq_max.popleft()
            if deq_min and deq_max:
                total_sum += nums[deq_min[0]] + nums[deq_max[0]]
            return total_sum
        total = 0
        for subarray_length in range(1, k + 1):
            deq_min = deque()
            deq_max = deque()
            for end in range(len(nums)):
                while deq_min and nums[deq_min[-1]] > nums[end]:
                    deq_min.pop()
                while deq_max and nums[deq_max[-1]] < nums[end]:
                    deq_max.pop()
                deq_min.append(end)
                deq_max.append(end)
                start = end - subarray_length + 1
                if start >= 0:
                    total += sum_of_deques(deq_min, deq_max, start, end)
        return str(total)