import pythoness
from typing import List

@pythoness.spec(
    """Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
 
Constraints:

n == height.length
1 <= n <= 2 * 10^4
0 <= height[i] <= 10^5""",
    tests=['trap(height = [0,1,0,2,1,0,1,3,2,1,2,1]) == 6'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def trap(height: List[int]) -> int:
    """"""

trap()