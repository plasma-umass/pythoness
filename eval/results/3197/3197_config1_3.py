import pythoness
from typing import List, Optional

def minimumSum(grid: List[List[int]]) -> int:
    """
    You are given a 2D binary array grid. You need to find 3 non-overlapping rectangles having non-zero areas with horizontal and vertical sides such that all the 1's in grid lie inside these rectangles.
    Return the minimum possible sum of the area of these rectangles.
    Note that the rectangles are allowed to touch.

    Constraints:

    1 <= grid.length, grid[i].length <= 30
    grid[i][j] is either 0 or 1.
    The input is generated such that there are at least three 1's in grid.
    """
    # Function to calculate the minimum enclosing rectangle for given 1's

    def min_enclosing_area(points):
        min_row = min((row for (row, col) in points))
        max_row = max((row for (row, col) in points))
        min_col = min((col for (row, col) in points))
        max_col = max((col for (row, col) in points))
        return (max_row - min_row + 1) * (max_col - min_col + 1)
    from itertools import combinations
    from sys import maxsize
    # Extract all 1's positions
    ones = [(i, j) for (i, row) in enumerate(grid) for (j, val) in enumerate(row) if val == 1]
    if len(ones) < 3:
        return 0
    min_area_sum = maxsize
    # Iterate over all combinations of splitting the 'ones' into 3 groups
    for comb1 in combinations(ones, len(ones) - 2):
        remaining1 = [pt for pt in ones if pt not in comb1]
        for comb2 in combinations(remaining1, len(remaining1) - 1):
            remaining2 = [pt for pt in remaining1 if pt not in comb2]
            if len(remaining2) == 1:  # Sanity check
                area1 = min_enclosing_area(comb1)
                area2 = min_enclosing_area(comb2)
                area3 = min_enclosing_area(remaining2)
                total_area = area1 + area2 + area3
                min_area_sum = min(min_area_sum, total_area)
    return min_area_sum
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])