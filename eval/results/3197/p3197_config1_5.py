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

    def get_ones_positions(grid):
        positions = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    positions.append((i, j))
        return positions

    def calculate_area(positions):
        (x_coords, y_coords) = zip(*positions)
        return (max(x_coords) - min(x_coords) + 1) * (max(y_coords) - min(y_coords) + 1)
    ones_positions = get_ones_positions(grid)
    if len(ones_positions) < 3:
        return 0
    from itertools import combinations
    min_area_sum = float('inf')
    # Try all combinations of dividing the 1s positions into 3 groups for 3 rectangles
    for split1 in range(1, len(ones_positions) - 1):
        for split2 in range(split1 + 1, len(ones_positions)):
            rect1_positions = ones_positions[:split1]
            rect2_positions = ones_positions[split1:split2]
            rect3_positions = ones_positions[split2:]
            area_sum = calculate_area(rect1_positions) + calculate_area(rect2_positions) + calculate_area(rect3_positions)
            min_area_sum = min(min_area_sum, area_sum)
    return min_area_sum
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])