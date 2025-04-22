import pythoness
from typing import List, Optional

class Solution:
    
    def separateSquares(self, squares: List[List[int]]) -> float:
        """
        Determines the minimum y-coordinate of a horizontal line that balances the area covered by squares above and below it.
        Each square is represented by its bottom-left corner coordinates and side length, with overlapping areas counted once.
        The algorithm accepts solutions with a precision within 10^-5 of the actual answer.
        """
    
        def areaBelowLine(y: float) -> float:
            area = 0.0
            for (x, bottom, side) in squares:
                top = bottom + side
                if y > top:
                    area += side * side
                elif y > bottom:
                    area += (y - bottom) * side
            return area
        # Find the minimal and maximal y-coordinate among provided squares
        min_y = min((bottom for (_, bottom, _) in squares))
        max_y = max((bottom + side for (_, bottom, side) in squares))
        # Binary search to find the critical line
        (low, high) = (min_y, max_y)
        total_area = sum((side * side for (_, _, side) in squares))
        target_area = total_area / 2.0
        while high - low > 1e-05:
            mid = (low + high) / 2.0
            if areaBelowLine(mid) < target_area:
                low = mid
            else:
                high = mid
        return (low + high) / 2.0