import pythoness
from typing import List, Optional

class Solution:
    
    def distanceSum(self, m: int, n: int, k: int) -> int:
        """
        Calculate the sum of Manhattan distances between all pairs of k identical pieces 
        placed on an m × n grid. Return the result for all valid arrangements of the 
        pieces, ensuring only one piece per cell, and the result modulo 10^9 + 7. 
        The function adheres to constraints: 1 <= m, n <= 10^5, 2 <= m * n <= 10^5, 
        2 <= k <= m * n.
        """
        MOD = 10 ** 9 + 7
        # Precompute cumulative row and column distances
        row_cumsum = [0] * m
        col_cumsum = [0] * n
        for i in range(1, m):
            row_cumsum[i] = row_cumsum[i - 1] + i
        for j in range(1, n):
            col_cumsum[j] = col_cumsum[j - 1] + j
        # Calculate total pairs
        total_pairs = k * (k - 1) // 2
        # Calculate total Manhattan distances for rows and columns
        total_row_distance = 0
        total_col_distance = 0
        for i in range(m):
            for j in range(n):
                # Number of positions remaining higher up in rows or columns
                row_remain = m - i - 1
                col_remain = n - j - 1
                # Calculate contribution by distances
                total_row_distance += row_remain * (n - j)
                total_col_distance += col_remain * (m - i)
        # Calculate result modulo MOD
        result = (total_row_distance + total_col_distance) * total_pairs % MOD
        return result