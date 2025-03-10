import pythoness
from typing import List


@pythoness.spec(
    """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.
Constraints:
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9""",
    tests=[
        "twoSum([2,7,11,15], 9) == [0,1]",
        "twoSum([3,2,4], 6) == [1,2]",
        "twoSum([3,3], 6) == [0,1]",
    ],
    test_descriptions=[],
    max_runtime=100,
    runtime=True,
    output=True,
    regenerate=True,
    verbose=True,
    # replace=True,
)
def twoSum(nums: List[int], target: int) -> List[int]:
    """"""


print(twoSum([2, 7, 11, 15], 9))
