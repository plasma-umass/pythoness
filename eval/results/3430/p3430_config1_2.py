import pythoness
from typing import List, Optional

class Solution:
    
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        """
        Calculate the sum of the maximum and minimum elements of all subarrays with at most k elements from an integer array nums.
    
        Constraints:
        1 <= nums.length <= 80000, 1 <= k <= nums.length, and -10^6 <= nums[i] <= 10^6.
        """
        # We'll use a double-ended queue (deque) to efficiently find the minimum and maximum of each subarray
        from collections import deque
    
        def sumOfMinMax(nums, k):
            result = 0
            n = len(nums)
            # Deques for tracking maximum and minimum
            maxDeque = deque()
            minDeque = deque()
            for i in range(n):
                # Remove elements not within range of k
                if maxDeque and maxDeque[0] <= i - k:
                    maxDeque.popleft()
                if minDeque and minDeque[0] <= i - k:
                    minDeque.popleft()
                # Maintain elements in maxDeque such that the values are in decreasing order
                while maxDeque and nums[maxDeque[-1]] <= nums[i]:
                    maxDeque.pop()
                maxDeque.append(i)
                # Maintain elements in minDeque such that the values are in increasing order
                while minDeque and nums[minDeque[-1]] >= nums[i]:
                    minDeque.pop()
                minDeque.append(i)
                # Calculate sum for subarrays of size up to k
                if i >= k - 1:
                    result += nums[maxDeque[0]] + nums[minDeque[0]]
            return result
        return sumOfMinMax(nums, k)