import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given an integer array nums, return the number of reverse pairs in the array.
A reverse pair is a pair (i, j) where:

0 <= i < j < nums.length and
nums[i] > 2 * nums[j].

 
Constraints:

1 <= nums.length <= 5 * 10^4
-2^31 <= nums[i] <= 2^31 - 1""",
    tests=['reversePairs(nums = [1,3,2,3,1]) == 2', 'reversePairs(nums = [2,4,3,5,1]) == 3'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def reversePairs(nums: List[int]) -> int:
    """"""

reversePairs(nums = [1,3,2,3,1]) 