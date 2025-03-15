import pythoness
from typing import List, Optional

def trap(height: List[int]) -> int:
    """
    Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

    Constraints:

    n == height.length
    1 <= n <= 2 * 10^4
    0 <= height[i] <= 10^5
    """
    if not height:
        return 0
    n = len(height)
    (left, right) = (0, n - 1)
    (left_max, right_max) = (height[left], height[right])
    water_trapped = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water_trapped += max(0, left_max - height[left])
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water_trapped += max(0, right_max - height[right])
    return water_trapped
trap(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])