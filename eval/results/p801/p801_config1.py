import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given two integer arrays of the same length nums1 and nums2. In one operation, you are allowed to swap nums1[i] with nums2[i].

For example, if nums1 = [1,2,3,8], and nums2 = [5,6,7,4], you can swap the element at i = 3 to obtain nums1 = [1,2,3,4] and nums2 = [5,6,7,8].

Return the minimum number of needed operations to make nums1 and nums2 strictly increasing. The test cases are generated so that the given input always makes it possible.
An array arr is strictly increasing if and only if arr[0] < arr[1] < arr[2] < ... < arr[arr.length - 1].
 
Constraints:

2 <= nums1.length <= 10^5
nums2.length == nums1.length
0 <= nums1[i], nums2[i] <= 2 * 10^5""",
    tests=['minSwap(nums1 = [1,3,5,4], nums2 = [1,2,3,7]) == 1', 'minSwap(nums1 = [0,3,5,8,9], nums2 = [2,1,4,6,9]) == 1'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minSwap(nums1: List[int], nums2: List[int]) -> int:
    """"""

minSwap(nums1 = [1,3,5,4], nums2 = [1,2,3,7]) 