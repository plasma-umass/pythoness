# file: src/oracle.py:1-23
# asked: {"lines": [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23], "branches": [[5, 6], [5, 8], [11, 0], [11, 12], [18, 19], [18, 20], [20, 21], [20, 23]]}
# gained: {"lines": [1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23], "branches": [[5, 6], [5, 8], [11, 12], [18, 19], [18, 20], [20, 23]]}

import pytest
from src.oracle4 import Solution


@pytest.fixture
def solution():
    return Solution()


def test_findMedianSortedArrays_case1(solution):
    nums1 = [1, 3]
    nums2 = [2]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 2.0


def test_findMedianSortedArrays_case2(solution):
    nums1 = [1, 2]
    nums2 = [3, 4]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 2.5


def test_findMedianSortedArrays_case3(solution):
    nums1 = [0, 0]
    nums2 = [0, 0]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 0.0


def test_findMedianSortedArrays_case4(solution):
    nums1 = []
    nums2 = [1]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 1.0


def test_findMedianSortedArrays_case5(solution):
    nums1 = [2]
    nums2 = []
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 2.0


def test_findMedianSortedArrays_case6(solution):
    nums1 = [1, 3]
    nums2 = [2, 7]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 2.5


def test_findMedianSortedArrays_case7(solution):
    nums1 = [1, 2, 3, 4]
    nums2 = [5, 6, 7, 8, 9]
    result = solution.findMedianSortedArrays(nums1, nums2)
    assert result == 5.0
