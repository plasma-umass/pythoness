import pythoness
from typing import List


@pythoness.spec(
    """Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.
You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
 
Constraints:

1 <= nums.length <= 10^5
-2^31 <= nums[i] <= 2^31 - 1""",
    tests=[
        "firstMissingPositive(nums = [1,2,0]) == 3",
        "firstMissingPositive(nums = [3,4,-1,1]) == 2",
        "firstMissingPositive(nums = [7,8,9,11,12]) == 1",
    ],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def firstMissingPositive(nums: List[int]) -> int:
    """"""


firstMissingPositive(nums=[1, 2, 0])
