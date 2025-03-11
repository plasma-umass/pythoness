import pythoness
from typing import List
from typing import List

def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
    The overall run time complexity should be O(log (m+n)).

    Constraints:

    nums1.length == m
    nums2.length == n
    0 <= m <= 1000
    0 <= n <= 1000
    1 <= m + n <= 2000
    -10^6 <= nums1[i], nums2[i] <= 10^6
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        (nums1, nums2) = (nums2, nums1)
    (x, y) = (len(nums1), len(nums2))
    (low, high) = (0, x)
    while low <= high:
        partitionX = (low + high) // 2
        partitionY = (x + y + 1) // 2 - partitionX
        # If partitionX is 0 it means nothing is there on left side. Use -inf for maxLeftX
        # If partitionX is length of input then there is nothing on right side. Use +inf for minRightX
        maxLeftX = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
        minRightX = float('inf') if partitionX == x else nums1[partitionX]
        maxLeftY = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
        minRightY = float('inf') if partitionY == y else nums2[partitionY]
        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            # We have found the median
            if (x + y) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2
            else:
                return max(maxLeftX, maxLeftY)
        elif maxLeftX > minRightY:
            # Move towards left in nums1
            high = partitionX - 1
        else:
            # Move towards right in nums1
            low = partitionX + 1
    # If we can't find any result and function wasn't returned above
    raise ValueError('Input arrays are invalid and do not form a valid partition')
findMedianSortedArrays(nums1=[1, 3], nums2=[2])