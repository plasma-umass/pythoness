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
    
        def calculate_area_up_to(y: float) -> float:
            total_area = 0
            for (x, y_bottom, side) in squares:
                y_top = y_bottom + side
                if y > y_bottom:
                    height_above_cutoff = min(y - y_bottom, side)
                    total_area += side * height_above_cutoff
            return total_area
        total_area = sum((side * side for (_, _, side) in squares))
        target_area = total_area / 2
        (low, high) = (min((y for (_, y, _) in squares)), max((y + side for (_, y, side) in squares)))
        while high - low > 1e-05:
            mid = (low + high) / 2
            area_below = calculate_area_up_to(mid)
            if area_below < target_area:
                low = mid
            else:
                high = mid
        return (low + high) / 2