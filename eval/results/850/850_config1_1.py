import pythoness
from typing import List, Optional

def rectangleArea(rectangles: List[List[int]]) -> int:
    """
    You are given a 2D array of axis-aligned rectangles. Each rectangle[i] = [xi1, yi1, xi2, yi2] denotes the i^th
    rectangle where (xi1, yi1) are the coordinates of the bottom-left corner, and (xi2, yi2) are the coordinates of the
    top-right corner.
    Calculate the total area covered by all rectangles in the plane. Any area covered by two or more rectangles should
    only be counted once.
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
    events = []  # x, open/close, y1, y2
    for (x1, y1, x2, y2) in rectangles:
        events.append((x1, 1, y1, y2))  # add event for opening rectangle
        events.append((x2, -1, y1, y2))  # add event for closing rectangle
    events.sort()  # Sort events by x coordinate

    def get_covered_length(active_intervals):
        """
        Calculate total length covered by a set of 1D active intervals.
        """
        length = 0
        prev_y = -1
        for (y1, y2) in active_intervals:
            prev_y = max(prev_y, y1)
            length += max(0, y2 - prev_y)
            prev_y = max(prev_y, y2)
        return length
    active_intervals = []
    prev_x = events[0][0]
    area = 0
    for (x, typ, y1, y2) in events:
        # Update area covered by all active intervals in the x-range [prev_x, x]
        area += (x - prev_x) * get_covered_length(active_intervals)
        area %= MOD
        # Update active_intervals: add or remove the current rectangle interval
        if typ == 1:
            active_intervals.append((y1, y2))
            active_intervals.sort()
        else:
            active_intervals.remove((y1, y2))
        prev_x = x
    return area
rectangleArea(rectangles=[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])