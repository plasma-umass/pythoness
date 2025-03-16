class Solution:
    import pythoness
    from typing import List, Optional
    
    def minimumSum(self, grid: List[List[int]]) -> int:
        """
        You are given a 2D binary array grid. You need to find 3 non-overlapping rectangles having non-zero areas with horizontal and vertical sides such that all the 1's in grid lie inside these rectangles.
        Return the minimum possible sum of the area of these rectangles.
        Note that the rectangles are allowed to touch.
    
        Constraints:
    
        1 <= grid.length, grid[i].length <= 30
        grid[i][j] is either 0 or 1.
        The input is generated such that there are at least three 1's in grid.
        """
        from itertools import combinations
    
        def calculate_area(rectangle):
            # Calculate area of a rectangle defined by (x_min, y_min, x_max, y_max)
            (x_min, y_min, x_max, y_max) = rectangle
            return (x_max - x_min + 1) * (y_max - y_min + 1)
    
        def get_bounding_rectangle(points):
            # Get the smallest rectangle that contains all points
            x_min = min((x for (x, y) in points))
            x_max = max((x for (x, y) in points))
            y_min = min((y for (x, y) in points))
            y_max = max((y for (x, y) in points))
            return (x_min, y_min, x_max, y_max)
        ones = [(i, j) for (i, row) in enumerate(grid) for (j, val) in enumerate(row) if val == 1]
        min_sum_area = float('inf')
        # Try all combinations to split points into three non-empty groups
        for split1 in range(1, len(ones) - 1):
            for split2 in range(split1 + 1, len(ones)):
                group1 = ones[:split1]
                group2 = ones[split1:split2]
                group3 = ones[split2:]
                # Calculate bounding rectangles
                rect1 = get_bounding_rectangle(group1)
                rect2 = get_bounding_rectangle(group2)
                rect3 = get_bounding_rectangle(group3)
                # Calculate sum of areas
                sum_area = calculate_area(rect1) + calculate_area(rect2) + calculate_area(rect3)
                min_sum_area = min(min_sum_area, sum_area)
        return min_sum_area