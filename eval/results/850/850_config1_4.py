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
    events = []
    for (x1, y1, x2, y2) in rectangles:
        events.append((x1, y1, y2, 1))
        events.append((x2, y1, y2, -1))
    events.sort()

    def calc_y_coverage(active_intervals):
        coverage = 0
        prev_y = -1
        for (y1, y2) in active_intervals:
            prev_y = max(prev_y, y1)
            coverage += max(0, y2 - prev_y)
            prev_y = max(prev_y, y2)
        return coverage
    from collections import defaultdict
    active_intervals = defaultdict(int)
    current_x = events[0][0]
    total_area = 0
    for (x, y1, y2, event_type) in events:
        total_area += (x - current_x) * calc_y_coverage(sorted(active_intervals.keys()))
        current_x = x
        if event_type == 1:
            active_intervals[y1, y2] += 1
        else:
            active_intervals[y1, y2] -= 1
            if active_intervals[y1, y2] == 0:
                del active_intervals[y1, y2]
    return total_area % MOD
rectangleArea(rectangles=[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])