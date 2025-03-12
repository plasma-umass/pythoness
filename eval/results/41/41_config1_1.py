import pythoness
from typing import List, Optional
from typing import List

def firstMissingPositive(nums: List[int]) -> int:
    """
    Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.
    You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.

    Constraints:

    1 <= nums.length <= 10^5
    -2^31 <= nums[i] <= 2^31 - 1
    """
    n = len(nums)
    # First pass, change all negative numbers and numbers greater than n to a number outside the range
    for i in range(n):
        if nums[i] <= 0 or nums[i] > n:
            nums[i] = n + 1
    # Second pass, use element index as a hash to record presence of numbers
    for i in range(n):
        num = abs(nums[i])
        if num <= n:
            idx = num - 1
            if nums[idx] > 0:
                nums[idx] = -nums[idx]
    # Third pass, find the first positive index
    for i in range(n):
        if nums[i] > 0:
            return i + 1
    return n + 1
firstMissingPositive(nums=[1, 2, 0])