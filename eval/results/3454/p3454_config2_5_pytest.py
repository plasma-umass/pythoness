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
        from collections import defaultdict
        # First, calculate the total area covered by any square
        events = []
        for (x, y, l) in squares:
            events.append((y, x, x + l, 1))  # square starts
            events.append((y + l, x, x + l, -1))  # square ends
        # Sort events based on y-coordinate
        events.sort()
        # Function to calculate combined x-coverage length
    
        def calculate_length(active_intervals):
            active_intervals.sort()
            total_length = 0
            current_start = -1
            for (start, end) in active_intervals:
                current_start = max(current_start, start)
                if end > current_start:
                    total_length += end - current_start
                    current_start = end
            return total_length
        previous_y = total_area = 0
        active_intervals = []
        for (y, x_start, x_end, typ) in events:
            # Process only after we have a previous point to refer to
            if active_intervals:
                length = calculate_length(active_intervals)
                total_area += length * (y - previous_y)
            # Update active intervals
            if typ == 1:
                active_intervals.append((x_start, x_end))  # Add interval
            else:
                active_intervals.remove((x_start, x_end))  # Remove interval
            previous_y = y
        # Binary search to find minimum y that splits total_area
        (left, right) = (0, max((y + l for (_, y, l) in squares)))
        target_area = total_area / 2
        while right - left > 1e-06:
            mid = (left + right) / 2
            active_intervals = []
            area_below = 0
            for (y, x_start, x_end, typ) in events:
                if y >= mid:
                    break
                if active_intervals:
                    length = calculate_length(active_intervals)
                    area_below += length * (y - previous_y)
                if typ == 1:
                    active_intervals.append((x_start, x_end))
                else:
                    active_intervals.remove((x_start, x_end))
                previous_y = y
            if area_below < target_area:
                left = mid
            else:
                right = mid
        return round(right, 5)