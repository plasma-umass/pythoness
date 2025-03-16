import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given two positive integer arrays nums and target, of the same length.
In a single operation, you can select any subarray of nums and increment each element within that subarray by 1 or decrement each element within that subarray by 1.
Return the minimum number of operations required to make nums equal to the array target.
 
Constraints:

1 <= nums.length == target.length <= 10^5
1 <= nums[i], target[i] <= 10^8""",
    tests=['minimumOperations(nums = [3,5,1,2], target = [4,6,2,4]) == 2', 'minimumOperations(nums = [1,3,2], target = [2,1,4]) == 5'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minimumOperations(nums: List[int], target: List[int]) -> int:
    """"""

minimumOperations(nums = [3,5,1,2], target = [4,6,2,4]) 