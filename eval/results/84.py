import pythoness
from typing import List

@pythoness.spec(
    """Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
 
Constraints:

1 <= heights.length <= 10^5
0 <= heights[i] <= 10^4""",
    tests=['largestRectangleArea(heights = [2,1,5,6,2,3]) == 10'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def largestRectangleArea(heights: List[int]) -> int:
    """"""

largestRectangleArea()