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
    
        def calculate_area(y: float) -> float:
            total_area = 0.0
            for square in squares:
                (x, y_square, size) = square
                y_top = y_square + size
                if y >= y_square and y < y_top:
                    total_area += (y_top - y) * size
                elif y >= y_top:
                    total_area += size * size
            return total_area
        # Establish search boundaries and total area
        y_min = min((square[1] for square in squares))
        y_max = max((square[1] + square[2] for square in squares))
        total_area = sum((size ** 2 for (_, _, size) in squares))
        # Binary search for the balancing line
        precision = 1e-05
        (low, high) = (y_min, y_max)
        while high - low > precision:
            mid = (low + high) / 2
            area_below = calculate_area(mid)
            if area_below * 2 < total_area:
                low = mid
            else:
                high = mid
        return (low + high) / 2