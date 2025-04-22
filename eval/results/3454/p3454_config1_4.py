import pythoness
from typing import List, Optional

class Solution:
    
    def separateSquares(self, squares: List[List[int]]) -> float:
        """
        Determines the minimum y-coordinate of a horizontal line that balances the area covered by squares above and below it.
        Each square is represented by its bottom-left corner coordinates and side length, with overlapping areas counted once.
        The algorithm accepts solutions with a precision within 10^-5 of the actual answer.
        """
        from typing import List
    
        def calculate_area_below(line_y, squares):
            """Calculates the total area covered by the squares below the line y-coordinate."""
            total_area = 0
            for (x, y, length) in squares:
                if y < line_y:
                    # Calculate the overlap area
                    overlap_height = max(0, min(line_y - y, length))
                    total_area += length * overlap_height
            return total_area
    
        def calculate_area_above(line_y, squares):
            """Calculates the total area covered by the squares above the line y-coordinate."""
            total_area = 0
            for (x, y, length) in squares:
                square_top = y + length
                if square_top > line_y:
                    # Calculate the overlap area
                    overlap_height = max(0, min(square_top - line_y, length))
                    total_area += length * overlap_height
            return total_area
        # We need to check the range of y-coordinates for all squares
        min_y = min((y for (_, y, _) in squares))
        max_y = max((y + length for (_, y, length) in squares))
        # Binary search for the y-coordinate that balances the area
        (low, high) = (min_y, max_y)
        precision = 1e-05
        while high - low > precision:
            mid = (low + high) / 2.0
            area_below = calculate_area_below(mid, squares)
            area_above = calculate_area_above(mid, squares)
            if area_below < area_above:
                low = mid
            else:
                high = mid
        return (low + high) / 2.0