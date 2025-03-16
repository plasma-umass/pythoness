import pythoness
from typing import List, Optional

def rectangleArea(rectangles: List[List[int]]) -> int:
    """
    You are given a 2D array of axis-aligned rectangles. Each rectangle[i] = [xi1, yi1, xi2, yi2] denotes the i^th rectangle where (xi1, yi1) are the coordinates of the bottom-left corner, and (xi2, yi2) are the coordinates of the top-right corner.
    Calculate the total area covered by all rectangles in the plane. Any area covered by two or more rectangles should only be counted once.
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
    # Sort events by x-coordinate
    events = []
    for (x1, y1, x2, y2) in rectangles:
        events.append((x1, y1, y2, 1))  # starting edge
        events.append((x2, y1, y2, -1))  # ending edge
    events.sort()
    # Compress y-coordinates
    ys = sorted(set((y for (_, y1, y2, _) in events for y in (y1, y2))))
    y_index = {y: i for (i, y) in enumerate(ys)}
    # Segment tree status
    count = [0] * (len(ys) - 1)
    last_x = events[0][0]
    area = 0
    for (x, y1, y2, typ) in events:
        # Calculate width since last event
        width = x - last_x
        # Calculate the total height of current coverage
        y_covered = 0
        for i in range(len(count)):
            if count[i] > 0:
                y_covered += ys[i + 1] - ys[i]
        # Add to total area
        area = (area + width * y_covered % MOD) % MOD
        # Update count status
        for i in range(y_index[y1], y_index[y2]):
            count[i] += typ
        # Move to the next event
        last_x = x
    return area
rectangleArea(rectangles=[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])