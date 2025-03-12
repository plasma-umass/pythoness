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

    def merge_and_count(nums, left, mid, right):
        # Create temporary arrays
        left_arr = nums[left:mid + 1]
        right_arr = nums[mid + 1:right + 1]
        # Merging and counting reverse pairs
        i = j = 0
        count = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= 2 * right_arr[j]:
                i += 1
            else:
                count += len(left_arr) - i
                j += 1
        # Merge the arrays
        i = j = 0
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                nums[k] = left_arr[i]
                i += 1
            else:
                nums[k] = right_arr[j]
                j += 1
            k += 1
        while i < len(left_arr):
            nums[k] = left_arr[i]
            i += 1
            k += 1
        while j < len(right_arr):
            nums[k] = right_arr[j]
            j += 1
            k += 1
        return count

    def merge_sort_and_count(nums, left, right):
        count = 0
        if left < right:
            mid = (left + right) // 2
            count += merge_sort_and_count(nums, left, mid)
            count += merge_sort_and_count(nums, mid + 1, right)
            count += merge_and_count(nums, left, mid, right)
        return count
    return merge_sort_and_count(nums, 0, len(nums) - 1)
reversePairs(nums=[1, 3, 2, 3, 1])