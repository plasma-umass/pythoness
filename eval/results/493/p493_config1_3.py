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

    def merge_and_count(arr, temp_arr, left, mid, right):
        i = left  # Starting index for left subarray
        j = mid + 1  # Starting index for right subarray
        k = left  # Starting index to be sorted
        inv_count = 0
        # Count reverse pairs
        while i <= mid and j <= right:
            if arr[i] > 2 * arr[j]:
                inv_count += mid - i + 1
                j += 1
            else:
                i += 1
        i = left
        j = mid + 1
        # Merge the two subarrays
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                temp_arr[k] = arr[j]
                j += 1
            k += 1
        # Copy the remaining elements of left subarray, if any
        while i <= mid:
            temp_arr[k] = arr[i]
            i += 1
            k += 1
        # Copy the remaining elements of right subarray, if any
        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1
        # Copy the sorted subarray into Original array
        for i in range(left, right + 1):
            arr[i] = temp_arr[i]
        return inv_count

    def merge_sort_and_count(arr, temp_arr, left, right):
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
            inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
            inv_count += merge_and_count(arr, temp_arr, left, mid, right)
        return inv_count
    n = len(nums)
    temp_arr = [0] * n
    return merge_sort_and_count(nums, temp_arr, 0, n - 1)
reversePairs(nums=[1, 3, 2, 3, 1])