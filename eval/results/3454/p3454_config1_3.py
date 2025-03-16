import pythoness
from typing import List, Optional

def separateSquares(squares: List[List[int]]) -> float:
    """
    You are given a 2D integer array squares. Each squares[i] = [xi, yi, li] represents the coordinates of the bottom-left point and the side length of a square parallel to the x-axis.
    Find the minimum y-coordinate value of a horizontal line such that the total area covered by squares above the line equals the total area covered by squares below the line.
    Answers within 10^-5 of the actual answer will be accepted.
    Note: Squares may overlap. Overlapping areas should be counted only once in this version.

    Constraints:

    1 <= squares.length <= 5 * 10^4
    squares[i] = [xi, yi, li]
    squares[i].length == 3
    0 <= xi, yi <= 10^9
    1 <= li <= 10^9
    The total area of all the squares will not exceed 10^15.
    """
    from bisect import bisect_right
    from collections import defaultdict
    events = []
    for (xi, yi, li) in squares:
        events.append((yi, xi, xi + li, 1))  # Entry event
        events.append((yi + li, xi, xi + li, -1))  # Exit event
    events.sort()
    active_intervals = []
    total_area = 0
    y_prev = events[0][0]
    interval_count = defaultdict(int)
    for (y, x_start, x_end, type) in events:
        # Calculate prior area
        active_intervals.sort()
        current_x = -1
        width = 0
        for (x_start_active, x_end_active) in active_intervals:
            current_x = max(current_x, x_start_active)
            width += max(0, x_end_active - current_x)
            current_x = max(current_x, x_end_active)
        total_area += width * (y - y_prev)
        y_prev = y
        # Update the list of active intervals
        if type == 1:
            interval_count[x_start, x_end] += 1
            if interval_count[x_start, x_end] == 1:
                active_intervals.append((x_start, x_end))
        else:
            interval_count[x_start, x_end] -= 1
            if interval_count[x_start, x_end] == 0:
                active_intervals.remove((x_start, x_end))
    target_area = total_area / 2
    current_area = 0
    active_intervals = []
    interval_count = defaultdict(int)
    prev_y = events[0][0]
    for (y, x_start, x_end, type) in events:
        width = 0
        active_intervals.sort()
        current_x = -1
        for (x_start_active, x_end_active) in active_intervals:
            current_x = max(current_x, x_start_active)
            width += max(0, x_end_active - current_x)
            current_x = max(current_x, x_end_active)
        if current_area + width * (y - prev_y) >= target_area:
            return prev_y + (target_area - current_area) / width
        current_area += width * (y - prev_y)
        prev_y = y
        if type == 1:
            interval_count[x_start, x_end] += 1
            if interval_count[x_start, x_end] == 1:
                active_intervals.append((x_start, x_end))
        else:
            interval_count[x_start, x_end] -= 1
            if interval_count[x_start, x_end] == 0:
                active_intervals.remove((x_start, x_end))
    return prev_y
separateSquares(squares=[[0, 0, 1], [2, 2, 1]])