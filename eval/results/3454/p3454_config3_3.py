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

    The function should pass the following tests:
        separateSquares(squares = [[0,0,1],[2,2,1]]) == 1.00000
        separateSquares(squares = [[0,0,2],[1,1,1]]) == 1.00000
    """

    def compute_area(y_line: float) -> float:
        from sortedcontainers import SortedList
        events = []
        for (x, y, l) in squares:
            events.append((y, x, x + l, 1))  # start of square
            events.append((y + l, x, x + l, -1))  # end of square
        events.sort()
        active_intervals = SortedList()
        prev_y = events[0][0]
        total_area = 0.0

        def compute_width() -> int:
            width = 0
            prev_x = -1
            for (x_start, x_end) in active_intervals:
                if prev_x < x_start:
                    width += x_end - x_start
                elif prev_x < x_end:
                    width += x_end - prev_x
                prev_x = max(prev_x, x_end)
            return width
        for (cur_y, x_start, x_end, delta) in events:
            if cur_y > y_line:
                break
            width = compute_width()
            total_area += width * (cur_y - prev_y)
            if delta == 1:
                active_intervals.add((x_start, x_end))
            else:
                active_intervals.remove((x_start, x_end))
            prev_y = cur_y
        return total_area
    low = 0
    high = max((yi + li for (_, yi, li) in squares))
    total_area = compute_area(high)
    target_area = total_area / 2
    while high - low > 1e-05:
        mid = (low + high) / 2
        if compute_area(mid) < target_area:
            low = mid
        else:
            high = mid
    return round((low + high) / 2, 5)
separateSquares(squares=[[0, 0, 1], [2, 2, 1]])