# file: src/oracle4.py:1-23
# asked: {"lines": [21], "branches": [[11, 0], [20, 21]]}
# gained: {"lines": [21], "branches": [[20, 21]]}

import pytest
from p4_config1_3_pytest import Solution


def test_findMedianSortedArrays_case1():
    solution = Solution()
    nums1 = [1, 3]
    nums2 = [2]
    expected_median = 2.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case2():
    solution = Solution()
    nums1 = [1, 2]
    nums2 = [3, 4]
    expected_median = 2.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case3():
    solution = Solution()
    nums1 = [0, 0]
    nums2 = [0, 0]
    expected_median = 0.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case4():
    solution = Solution()
    nums1 = []
    nums2 = [1]
    expected_median = 1.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case5():
    solution = Solution()
    nums1 = [2]
    nums2 = []
    expected_median = 2.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case6():
    solution = Solution()
    nums1 = [1, 3, 8, 9, 15]
    nums2 = [7, 11, 18, 19, 21, 25]
    expected_median = 11.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case7():
    solution = Solution()
    nums1 = [23, 26, 31, 35]
    nums2 = [3, 5, 7, 9, 11, 16]
    expected_median = 13.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median


def test_findMedianSortedArrays_case8():
    solution = Solution()
    nums1 = [1, 2, 3, 4, 5, 6]
    nums2 = [7, 8, 9, 10, 11, 12]
    expected_median = 6.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_median
