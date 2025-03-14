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
    # To apply the sweep line algorithm
    events = []
    for (x1, y1, x2, y2) in rectangles:
        events.append((y1, x1, x2, 1))  # open the rectangle
        events.append((y2, x1, x2, -1))  # close the rectangle
    # Sort events by y, and by type (-1 before 1 at same y)
    events.sort()
    # Active x-coordinates with a count of how many rectangles are covering it
    active = []

    def query():
        # Calculate total length covered at current y
        current_length = 0
        current_right = -1
        for (x1, x2) in active:
            current_right = max(current_right, x1)
            current_length += max(0, x2 - current_right)
            current_right = max(current_right, x2)
        return current_length
    last_y = 0
    area = 0
    for (y, x1, x2, typ) in events:
        # Calculate area added since last event
        area += query() * (y - last_y)
        area %= MOD
        # Update the active set
        if typ == 1:
            active.append((x1, x2))
            active.sort()
        else:
            active.remove((x1, x2))
        last_y = y
    return area
rectangleArea(rectangles=[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])