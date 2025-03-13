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

    def calculate_area(points):
        min_x = min((p[0] for p in points))
        max_x = max((p[0] for p in points))
        min_y = min((p[1] for p in points))
        max_y = max((p[1] for p in points))
        return (max_x - min_x + 1) * (max_y - min_y + 1)
    ones = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 1]
    min_sum_area = float('inf')
    # Iterate over all possible ways to partition ones into 3 parts
    for comb in combinations(range(len(ones)), len(ones) - 3 + 1):
        subset1 = [ones[i] for i in range(len(ones)) if i in comb]
        rem_ones = [ones[i] for i in range(len(ones)) if i not in comb]
        for comb2 in combinations(range(len(rem_ones)), len(rem_ones) - 2 + 1):
            subset2 = [rem_ones[i] for i in range(len(rem_ones)) if i in comb2]
            subset3 = [rem_ones[i] for i in range(len(rem_ones)) if i not in comb2]
            area1 = calculate_area(subset1)
            area2 = calculate_area(subset2)
            area3 = calculate_area(subset3)
            min_sum_area = min(min_sum_area, area1 + area2 + area3)
    return min_sum_area
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])