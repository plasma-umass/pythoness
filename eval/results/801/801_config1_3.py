import pythoness
from typing import List, Optional

def minSwap(nums1: List[int], nums2: List[int]) -> int:
    """
    You are given two integer arrays of the same length nums1 and nums2. In one operation, you are allowed to swap nums1[i] with nums2[i].

    For example, if nums1 = [1,2,3,8], and nums2 = [5,6,7,4], you can swap the element at i = 3 to obtain nums1 = [1,2,3,4] and nums2 = [5,6,7,8].

    Return the minimum number of needed operations to make nums1 and nums2 strictly increasing. The test cases are generated so that the given input always makes it possible.
    An array arr is strictly increasing if and only if arr[0] < arr[1] < arr[2] < ... < arr[arr.length - 1].

    Constraints:

    2 <= nums1.length <= 10^5
    nums2.length == nums1.length
    0 <= nums1[i], nums2[i] <= 2 * 10^5
    """
    n = len(nums1)
    # Initialize two arrays to store the minimum swaps.
    # no_swap[i] means the minimum swaps if we do not swap nums1[i] and nums2[i].
    # swap[i] means the minimum swaps if we swap nums1[i] and nums2[i].
    no_swap = [float('inf')] * n
    swap = [float('inf')] * n
    # At the first position, we don't need to swap, so the initial condition:
    no_swap[0] = 0
    swap[0] = 1
    # Iterate through all positions from 1 to n-1
    for i in range(1, n):
        # Both arrays are strictly increasing without swap or swap both
        if nums1[i] > nums1[i - 1] and nums2[i] > nums2[i - 1]:
            no_swap[i] = no_swap[i - 1]
            swap[i] = swap[i - 1] + 1
        # Arrays are strictly increasing if nums1[i] swapped with nums2[i-1]
        # and nums2[i] swapped with nums1[i-1]
        if nums1[i] > nums2[i - 1] and nums2[i] > nums1[i - 1]:
            no_swap[i] = min(no_swap[i], swap[i - 1])
            swap[i] = min(swap[i], no_swap[i - 1] + 1)
    # The answer is the minimum of the last elements of both arrays
    return min(no_swap[-1], swap[-1])
minSwap(nums1=[1, 3, 5, 4], nums2=[1, 2, 3, 7])