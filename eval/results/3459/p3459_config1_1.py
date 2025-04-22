import pythoness
from typing import List, Optional

class Solution:
    
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        """
        Finds the length of the longest V-shaped diagonal segment in a 2D integer matrix,
        where each segment starts with 1 and follows the sequence 2, 0, 2, 0...
        along a diagonal. The segment can change direction once by a 90-degree clockwise turn
        while maintaining the sequence. Returns the length of the longest valid segment or 0
        if no segment exists.
        """
        if not grid or not grid[0]:
            return 0
        (rows, cols) = (len(grid), len(grid[0]))
        max_length = 0
        # Function to check the length of diagonal with direction and position
    
        def check_diagonal(x, y, dx, dy, seq):
            length = 0
            seq_index = 0
            while 0 <= x < rows and 0 <= y < cols:
                if grid[x][y] == seq[seq_index]:
                    length += 1
                    seq_index = (seq_index + 1) % len(seq)
                else:
                    break
                x += dx
                y += dy
            return length
        seq_1 = [1, 2, 0, 2, 0]  # Sequence pattern we are looking for
        # Try all starting points (1s) in the grid and check both possible V-paths
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # Option 1: Start going down-right
                    length_1 = check_diagonal(i, j, 1, 1, seq_1)  # Primary diagonal
                    # Turn clockwise to down-left
                    if length_1 > 2:
                        further_length = check_diagonal(i + 2, j + 2, 1, -1, seq_1[2:])
                        max_length = max(max_length, length_1 + further_length - 2)
                    max_length = max(max_length, length_1)
                    # Option 2: Start going down-left
                    length_2 = check_diagonal(i, j, 1, -1, seq_1)  # Counter-diagonal
                    # Turn clockwise to down-right
                    if length_2 > 2:
                        further_length = check_diagonal(i + 2, j - 2, 1, 1, seq_1[2:])
                        max_length = max(max_length, length_2 + further_length - 2)
                    max_length = max(max_length, length_2)
        return max_length