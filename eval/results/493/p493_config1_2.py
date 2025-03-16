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

    def merge_and_count(nums, temp, left, mid, right):
        (i, j, k) = (left, mid + 1, left)
        count = 0
        while i <= mid and j <= right:
            if nums[i] > 2 * nums[j]:
                count += mid - i + 1
                j += 1
            else:
                i += 1
        (i, j, k) = (left, mid + 1, left)
        while i <= mid and j <= right:
            if nums[i] <= nums[j]:
                temp[k] = nums[i]
                i += 1
            else:
                temp[k] = nums[j]
                j += 1
            k += 1
        while i <= mid:
            temp[k] = nums[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = nums[j]
            j += 1
            k += 1
        for i in range(left, right + 1):
            nums[i] = temp[i]
        return count

    def merge_sort_and_count(nums, temp, left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        count = merge_sort_and_count(nums, temp, left, mid)
        count += merge_sort_and_count(nums, temp, mid + 1, right)
        count += merge_and_count(nums, temp, left, mid, right)
        return count
    n = len(nums)
    temp = [0] * n
    return merge_sort_and_count(nums, temp, 0, n - 1)
reversePairs(nums=[1, 3, 2, 3, 1])