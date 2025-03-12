import pythoness
from typing import List, Optional
from typing import List

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
    left_max = [0] * n
    right_max = [0] * n
    water_trapped = 0
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    for i in range(n):
        water_trapped += min(left_max[i], right_max[i]) - height[i]
    return water_trapped
trap(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])