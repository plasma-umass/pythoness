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
    # Helper function to extract all positions of 1s

    def extract_ones_positions(grid):
        ones_positions = set()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    ones_positions.add((i, j))
        return ones_positions
    # Find the bounding box area for a set of positions

    def bounding_box_area(positions):
        min_x = min((pos[0] for pos in positions))
        max_x = max((pos[0] for pos in positions))
        min_y = min((pos[1] for pos in positions))
        max_y = max((pos[1] for pos in positions))
        return (max_x - min_x + 1) * (max_y - min_y + 1)
    ones_positions = extract_ones_positions(grid)
    min_area_sum = float('inf')
    # Try all ways to split the set of ones into 3 disjoint sets
    for combo1 in combinations(ones_positions, len(ones_positions) // 3):
        remaining = ones_positions - set(combo1)
        for combo2 in combinations(remaining, len(remaining) // 2):
            combo3 = remaining - set(combo2)
            area_sum = bounding_box_area(combo1) + bounding_box_area(combo2) + bounding_box_area(combo3)
            if area_sum < min_area_sum:
                min_area_sum = area_sum
    return min_area_sum
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])