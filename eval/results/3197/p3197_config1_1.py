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
    import itertools
    (rows, cols) = (len(grid), len(grid[0]))
    ones = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 1]

    def area(rect):
        (top_left, bottom_right) = rect
        (r1, c1) = top_left
        (r2, c2) = bottom_right
        return (r2 - r1 + 1) * (c2 - c1 + 1)

    def is_valid(ones, rectangles):
        covered = set()
        for ((r1, c1), (r2, c2)) in rectangles:
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    covered.add((r, c))
        return all((one in covered for one in ones))
    min_sum_area = float('inf')
    for rects in itertools.combinations(itertools.product(range(rows), range(cols), range(rows), range(cols)), 3):
        rectangles = []
        for (r1, c1, r2, c2) in rects:
            if r1 <= r2 and c1 <= c2:
                rectangles.append(((r1, c1), (r2, c2)))
        if len(rectangles) == 3 and is_valid(ones, rectangles):
            sum_area = sum((area(rect) for rect in rectangles))
            min_sum_area = min(min_sum_area, sum_area)
    return min_sum_area
minimumSum(grid=[[1, 0, 1], [1, 1, 1]])