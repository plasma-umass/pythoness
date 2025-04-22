import pythoness
from typing import List, Optional

@pythoness.spec(
    """Calculate the sum of the maximum and minimum elements of all subarrays with at most k elements from an integer array nums.

Constraints:
1 <= nums.length <= 80000, 1 <= k <= nums.length, and -10^6 <= nums[i] <= 10^6.""",
    tests=["""minMaxSubarraySum(**{'nums': [1, 2, 3, 4, 5], 'k': 3}) == '72'""", """minMaxSubarraySum(**{'nums': [1000000, -1000000], 'k': 1}) == '0'""", """minMaxSubarraySum(**{'nums': [1, -1, 2, -2, 3, -3, 4, -4, 5, -5], 'k': 4}) == '11'""", """minMaxSubarraySum(**{'nums': [999999, -999999, 0, 999999], 'k': 3}) == '1999998'""", """minMaxSubarraySum(**{'nums': [-1000000], 'k': 1}) == '-2000000'""", """minMaxSubarraySum(**{'nums': [1, -1, 1, -1, 1, -1, 1, -1], 'k': 8}) == '0'""", """minMaxSubarraySum(**{'nums': [50000, 49999, 50001, -50000, -49999, -50001], 'k': 3}) == '3'""", """minMaxSubarraySum(**{'nums': [-1, 1, -1, 1], 'k': 2}) == '0'""", """minMaxSubarraySum(**{'nums': [20], 'k': 1}) == '40'""", """minMaxSubarraySum(**{'nums': [7, 8, 5, 6, 9, 4], 'k': 5}) == '265'"""],
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minMaxSubarraySum(nums: List[int], k: int) -> int:
    """"""

minMaxSubarraySum(**{'nums': [1, 2, 3, 4, 5], 'k': 3}) 