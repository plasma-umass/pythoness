import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given a 2D binary array grid. You need to find 3 non-overlapping rectangles having non-zero areas with horizontal and vertical sides such that all the 1's in grid lie inside these rectangles.
Return the minimum possible sum of the area of these rectangles.
Note that the rectangles are allowed to touch.
 
Constraints:

1 <= grid.length, grid[i].length <= 30
grid[i][j] is either 0 or 1.
The input is generated such that there are at least three 1's in grid.""",
    tests=['minimumSum(grid = [[1,0,1],[1,1,1]]) == 5', 'minimumSum(grid = [[1,0,1,0],[0,1,0,1]]) == 5'],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minimumSum(grid: List[List[int]]) -> int:
    """"""

minimumSum(grid = [[1,0,1],[1,1,1]]) 