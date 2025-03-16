import pythoness
from typing import List, Optional

def reversePairs(nums: List[int]) -> int:
    """
    Given an integer array nums, return the number of reverse pairs in the array.
    A reverse pair is a pair (i, j) where:

    0 <= i < j < nums.length and
    nums[i] > 2 * nums[j].


    Constraints:

    1 <= nums.length <= 5 * 10^4
    -2^31 <= nums[i] <= 2^31 - 1
    """

    def merge_sort_and_count(arr, left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        count = merge_sort_and_count(arr, left, mid) + merge_sort_and_count(arr, mid + 1, right)
        j = mid + 1
        # Count the reverse pairs
        for i in range(left, mid + 1):
            while j <= right and arr[i] > 2 * arr[j]:
                j += 1
            count += j - (mid + 1)
        # Merge step
        arr[left:right + 1] = sorted(arr[left:right + 1])
        return count
    return merge_sort_and_count(nums, 0, len(nums) - 1)
reversePairs(nums=[1, 3, 2, 3, 1])