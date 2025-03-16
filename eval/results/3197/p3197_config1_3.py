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
    from itertools import combinations, product
    # List to store the positions of all the 1's in the grid
    ones = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 1]
    # If there are less than 3 ones, return 0 as it's not possible to form 3 rectangles
    if len(ones) < 3:
        return 0

    def calculate_area(x1, y1, x2, y2):
        """Calculate area of a rectangle defined by its corners (inclusive)"""
        return (x2 - x1 + 1) * (y2 - y1 + 1)

    def is_covered(sub_ones, rects):
        """Check if all positions in sub_ones are covered by the rectangles in rects"""
        covered = set()
        for (x1, y1, x2, y2) in rects:
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    covered.add((x, y))
        return all((point in covered for point in sub_ones))
    min_sum_area = float('inf')
    # Evaluate all combinations for three 1's to form the basis of three rectangles
    for inds in combinations(range(len(ones)), 3):
        ((x1, y1), (x2, y2), (x3, y3)) = (ones[inds[0]], ones[inds[1]], ones[inds[2]])
        # Boundaries for each rectangle
        for (x1_end, y1_end) in product(range(x1, len(grid)), range(y1, len(grid[0]))):
            if grid[x1_end][y1_end] != 1:
                continue
            for (x2_end, y2_end) in product(range(x2, len(grid)), range(y2, len(grid[0]))):
                if grid[x2_end][y2_end] != 1:
                    continue
                for (x3_end, y3_end) in product(range(x3, len(grid)), range(y3, len(grid[0]))):
                    if grid[x3_end][y3_end] != 1:
                        continue
                    # Define rectangles
                    rects = [(x1, y1, x1_end, y1_end), (x2, y2, x2_end, y2_end), (x3, y3, x3_end, y3_end)]
                    # Check whether all 1's are covered
                    if is_covered(ones, rects):
                        # Calculate sum of areas
                        area_sum = sum((calculate_area(*rect) for rect in rects))
                        # Update minimum area sum
                        min_sum_area = min(min_sum_area, area_sum)
    return min_sum_area
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])