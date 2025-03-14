import pythoness
from typing import List, Optional

def rectangleArea(rectangles: List[List[int]]) -> int:
    """
    You are given a 2D array of axis-aligned rectangles. Each rectangle[i] = [xi1, yi1, xi2, yi2]
    denotes the i^th rectangle where (xi1, yi1) are the coordinates of the bottom-left corner,
    and (xi2, yi2) are the coordinates of the top-right corner.
    Calculate the total area covered by all rectangles in the plane. Any area covered by two
    or more rectangles should only be counted once.
    Return the total area. Since the answer may be too large, return it modulo 10^9 + 7.

    Constraints:

    1 <= rectangles.length <= 200
    rectanges[i].length == 4
    0 <= xi1, yi1, xi2, yi2 <= 10^9
    xi1 <= xi2
    yi1 <= yi2
    All rectangles have non zero area.
    """
    MOD = 10 ** 9 + 7
    # Step 1: Collect all x and y coordinates
    x_coords = set()
    y_coords = set()
    for (x1, y1, x2, y2) in rectangles:
        x_coords.add(x1)
        x_coords.add(x2)
        y_coords.add(y1)
        y_coords.add(y2)
    # Step 2: Transform coordinates into sorted lists
    x_list = sorted(x_coords)
    y_list = sorted(y_coords)
    # Step 3: Create a mapping from coordinate to index
    x_index = {v: i for (i, v) in enumerate(x_list)}
    y_index = {v: i for (i, v) in enumerate(y_list)}
    # Step 4: Create a boolean grid representing covered areas
    grid = [[False] * len(y_list) for _ in range(len(x_list))]
    # Step 5: Fill in the grid based on rectangles
    for (x1, y1, x2, y2) in rectangles:
        for x in range(x_index[x1], x_index[x2]):
            for y in range(y_index[y1], y_index[y2]):
                grid[x][y] = True
    # Step 6: Calculate covered area
    total_area = 0
    for x in range(len(x_list) - 1):
        for y in range(len(y_list) - 1):
            if grid[x][y]:
                total_area += (x_list[x + 1] - x_list[x]) * (y_list[y + 1] - y_list[y])
                total_area %= MOD
    return total_area
rectangleArea(rectangles=[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])