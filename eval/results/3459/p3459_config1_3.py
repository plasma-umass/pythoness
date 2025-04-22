import pythoness
from typing import List, Optional

class Solution:
    
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Finds the length of the longest V-shaped diagonal segment in a 2D integer matrix, where each segment starts with 1 and follows the sequence 2, 0, 2, 0... along a diagonal. The segment can change direction once by a 90-degree clockwise turn while maintaining the sequence. Returns the length of the longest valid segment or 0 if no segment exists.
        """
        if not grid or not grid[0]:
            return 0
    
        def check_diagonal(x, y, dx, dy):
            length = 0
            expected_value = 1
            while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                if grid[x][y] == expected_value:
                    length += 1
                    expected_value = 2 if expected_value == 1 else 0 if expected_value == 2 else 2
                else:
                    break
                x += dx
                y += dy
            return length
        max_length = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    # Check diagonal down-right
                    length1 = check_diagonal(i, j, 1, 1)
                    # Check diagonal down-left
                    length2 = check_diagonal(i, j, 1, -1)
                    max_length = max(max_length, length1, length2)
        return max_length