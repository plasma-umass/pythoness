class Solution:
    import pythoness
    from typing import List, Optional
    
    def minimumSum(self, grid: List[List[int]]) -> int:
        """
        You are given a 2D binary array grid. You need to find 3 non-overlapping rectangles having non-zero areas with
        horizontal and vertical sides such that all the 1's in grid lie inside these rectangles.
        Return the minimum possible sum of the area of these rectangles.
        Note that the rectangles are allowed to touch.
    
        Constraints:
    
        1 <= grid.length, grid[i].length <= 30
        grid[i][j] is either 0 or 1.
        The input is generated such that there are at least three 1's in grid.
        """
        import itertools
        import sys
        (rows, cols) = (len(grid), len(grid[0]))
        one_positions = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
        # calculate minimum sum area of 3 rectangles that cover all '1's
    
        def min_area_3_rects(positions):
            min_area = sys.maxsize
            n = len(positions)
            # Try every possible combination to split the ones into three groups
            for split1 in range(1, n - 1):
                for split2 in range(split1 + 1, n):
                    (group1, group2, group3) = (positions[:split1], positions[split1:split2], positions[split2:])
                    area1 = calculate_area(group1)
                    area2 = calculate_area(group2)
                    area3 = calculate_area(group3)
                    total_area = area1 + area2 + area3
                    min_area = min(min_area, total_area)
            return min_area
        # Calculate the area of a rectangle that covers all points in `positions`
    
        def calculate_area(positions):
            if not positions:
                return 0
            min_row = min((r for (r, c) in positions))
            max_row = max((r for (r, c) in positions))
            min_col = min((c for (r, c) in positions))
            max_col = max((c for (r, c) in positions))
            return (max_row - min_row + 1) * (max_col - min_col + 1)
        return min_area_3_rects(one_positions)