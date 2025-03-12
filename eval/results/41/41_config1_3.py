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
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            (nums[nums[i] - 1], nums[i]) = (nums[i], nums[nums[i] - 1])
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
firstMissingPositive(nums=[1, 2, 0])