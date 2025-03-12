import pythoness
from typing import List, Optional

def validSubarraySize(nums: List[int], threshold: int) -> int:
    """
    You are given an integer array nums and an integer threshold.
    Find any subarray of nums of length k such that every element in the subarray is greater than threshold / k.
    Return the size of any such subarray. If there is no such subarray, return -1.
    A subarray is a contiguous non-empty sequence of elements within an array.

    Constraints:

    1 <= nums.length <= 10^5
    1 <= nums[i], threshold <= 10^9
    """
    n = len(nums)
    for k in range(1, n + 1):
        limit = threshold / k
        # Check if there is any subarray of length k where all elements satisfy the condition
        for i in range(n - k + 1):
            if all((x > limit for x in nums[i:i + k])):
                return k
    return -1
validSubarraySize(nums=[1, 3, 4, 3, 1], threshold=6)