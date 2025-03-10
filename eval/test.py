import pythoness
import typing

class Solution:

    @pythoness.spec(
        """Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log (m+n)).
 
Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-10^6 <= nums1[i], nums2[i] <= 10^6""",
        tests=["findMedianSortedArrays(nums1 = [1,3], nums2 = [2]) == 2.00000", "findMedianSortedArrays(nums1 = [1,2], nums2 = [3,4]) == 2.50000"],
        llm_unit=False,
        llm_prop=False,
        regenerate=True,
        verbose=True,
        output=True,
    )
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """"""

Solution.findMedianSortedArrays()