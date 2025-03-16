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
    from itertools import combinations
    # Collect all positions of 1s in the grid
    ones_positions = [(i, j) for (i, row) in enumerate(grid) for (j, value) in enumerate(row) if value == 1]

    def rect_area(p1, p2):
        return (p2[0] - p1[0] + 1) * (p2[1] - p1[1] + 1)

    def get_enclosing_rectangle(positions):
        min_row = min((pos[0] for pos in positions))
        max_row = max((pos[0] for pos in positions))
        min_col = min((pos[1] for pos in positions))
        max_col = max((pos[1] for pos in positions))
        return ((min_row, min_col), (max_row, max_col))

    def is_non_overlapping(rects):
        for (r1, r2) in combinations(rects, 2):
            (r1_min, r1_max) = r1
            (r2_min, r2_max) = r2
            if not (r1_max[0] < r2_min[0] or r1_min[0] > r2_max[0] or r1_max[1] < r2_min[1] or (r1_min[1] > r2_max[1])):
                return False
        return True
    min_area_sum = float('inf')
    for split1 in range(1, len(ones_positions) - 1):
        for split2 in range(split1 + 1, len(ones_positions)):
            first_group = ones_positions[:split1]
            second_group = ones_positions[split1:split2]
            third_group = ones_positions[split2:]
            rect1 = get_enclosing_rectangle(first_group)
            rect2 = get_enclosing_rectangle(second_group)
            rect3 = get_enclosing_rectangle(third_group)
            if is_non_overlapping([rect1, rect2, rect3]):
                area_sum = rect_area(*rect1) + rect_area(*rect2) + rect_area(*rect3)
                min_area_sum = min(min_area_sum, area_sum)
    return min_area_sum
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])