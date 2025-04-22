import pythoness
from typing import List, Optional

class Solution:
    
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Finds the length of the longest V-shaped diagonal segment in a 2D integer matrix, where each segment starts with 1 and follows the sequence 2, 0, 2, 0... along a diagonal. The segment can change direction once by a 90-degree clockwise turn while maintaining the sequence. Returns the length of the longest valid segment or 0 if no segment exists.
        """
        if not grid or not grid[0]:
            return 0
        (rows, cols) = (len(grid), len(grid[0]))
        sequence = [1, 2, 0]
        max_length = 0
    
        def check_direction(r, c, dir_r, dir_c, seq_idx):
            length = 0
            while 0 <= r < rows and 0 <= c < cols and (grid[r][c] == sequence[seq_idx % len(sequence)]):
                length += 1
                seq_idx += 1
                r += dir_r
                c += dir_c
            return length
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    # Check diagonals in "\" direction
                    length1 = check_direction(r, c, 1, 1, 0)  # Down-right
                    length2 = check_direction(r, c, 1, -1, 0)  # Down-left
                    # Check diagonals in "/" direction
                    length3 = check_direction(r, c, -1, 1, 0)  # Up-right
                    length4 = check_direction(r, c, -1, -1, 0)  # Up-left
                    # Combine V shapes
                    # Final shape: Up-right and Down-right, or Up-left and Down-left
                    combined_length1 = check_direction(r, c, -1, 1, 0) + check_direction(r + 1, c + 1, 1, 1, 1)
                    combined_length2 = check_direction(r, c, -1, -1, 0) + check_direction(r + 1, c - 1, 1, -1, 1)
                    max_length = max(max_length, length1, length2, length3, length4, combined_length1, combined_length2)
        return max_length