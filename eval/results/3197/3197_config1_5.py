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
    # Flatten the grid to get all the positions of 1s
    ones = [(i, j) for (i, row) in enumerate(grid) for (j, val) in enumerate(row) if val == 1]
    n = len(ones)
    # We need at least 3 rectangles
    if n < 3:
        return 0  # edge case that should not happen due to problem constraints
    # Initialize the minimum area sum to a large number
    min_area_sum = float('inf')
    # Generate all possible combinations of splitting the 1s into 3 groups
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            # First rectangle includes ones[0] to ones[i-1]
            # Second rectangle includes ones[i] to ones[j-1]
            # Third rectangle includes ones[j] to ones[n-1]
            rect1 = ones[:i]
            rect2 = ones[i:j]
            rect3 = ones[j:]
            # Compute area of each rectangle necessary to cover the points

            def compute_area(points):
                min_x = min((p[0] for p in points))
                max_x = max((p[0] for p in points))
                min_y = min((p[1] for p in points))
                max_y = max((p[1] for p in points))
                return (max_x - min_x + 1) * (max_y - min_y + 1)
            area_sum = compute_area(rect1) + compute_area(rect2) + compute_area(rect3)
            # Update the minimum area sum
            min_area_sum = min(min_area_sum, area_sum)
    return min_area_sum
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])