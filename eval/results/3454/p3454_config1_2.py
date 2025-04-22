import pythoness
from typing import List, Optional

class Solution:
    
    def separateSquares(self, squares: List[List[int]]) -> float:
        """
        Determines the minimum y-coordinate of a horizontal line that balances the area covered by squares above and below it.
        Each square is represented by its bottom-left corner coordinates and side length, with overlapping areas counted once.
        The algorithm accepts solutions with a precision within 10^-5 of the actual answer.
        """
    
        def calculate_area_above(y_coord, squares):
            area = 0.0
            for (x, y, side) in squares:
                if y + side > y_coord:
                    area += (y + side - y_coord) * side
                else:
                    continue
            return area
    
        def calculate_area_below(y_coord, squares):
            area = 0.0
            for (x, y, side) in squares:
                if y < y_coord:
                    area += (y_coord - y) * side
                else:
                    continue
            return area
        min_y = min((y for (_, y, _) in squares))
        max_y = max((y + side for (_, y, side) in squares))
        (left, right) = (min_y, max_y)
        precision = 1e-05
        while right - left > precision:
            mid = (left + right) / 2
            area_above_mid = calculate_area_above(mid, squares)
            area_below_mid = calculate_area_below(mid, squares)
            if area_above_mid > area_below_mid:
                left = mid
            else:
                right = mid
        return (left + right) / 2