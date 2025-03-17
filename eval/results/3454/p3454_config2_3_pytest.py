import pythoness
from typing import List, Optional

class Solution:
    
    def separateSquares(self, squares: List[List[int]]) -> float:
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
        from typing import List
        # Calculate total area covered by the squares considering overlap
        events = []
        for (xi, yi, li) in squares:
            events.append((yi, xi, xi + li, 1))  # square starts
            events.append((yi + li, xi, xi + li, -1))  # square ends
        # Sort by y coordinate, and by event type for events with the same y (start before end)
        events.sort()
        total_area = 0
        prev_y = events[0][0]
        active_intervals = []
        # Process events
    
        def calculate_active_area():
            active_intervals.sort()
            merged_intervals = []
            start = -1
            for (l, r) in active_intervals:
                if l > start:
                    merged_intervals.append([l, r])
                    start = r
                else:
                    merged_intervals[-1][1] = max(merged_intervals[-1][1], r)
                    start = merged_intervals[-1][1]
            area = sum((r - l for (l, r) in merged_intervals))
            return area
        for (y, x_start, x_end, typ) in events:
            # Calculate area covered since the last y-coordinate
            if y != prev_y:
                covered_length = calculate_active_area()
                total_area += covered_length * (y - prev_y)
                prev_y = y
            # Process current event
            if typ == 1:  # start of a square
                active_intervals.append((x_start, x_end))
            else:  # end of a square
                active_intervals.remove((x_start, x_end))
        # Binary search for the minimum y-coordinate
        (low, high) = (0, 10 ** 9)
        target_area = total_area / 2.0
        while high - low > 1e-05:
            mid_y = (low + high) / 2.0
            # Calculate area below y=mid_y
            active_intervals = []
            prev_y = events[0][0]
            area_below = 0
            for (y, x_start, x_end, typ) in events:
                if y >= mid_y:
                    break
                if y != prev_y:
                    covered_length = calculate_active_area()
                    area_below += covered_length * (y - prev_y)
                    prev_y = y
                if typ == 1:
                    active_intervals.append((x_start, x_end))
                else:
                    active_intervals.remove((x_start, x_end))
            # Compare area below mid_y with target area
            if area_below < target_area:
                low = mid_y
            else:
                high = mid_y
        return round((low + high) / 2.0, 5)