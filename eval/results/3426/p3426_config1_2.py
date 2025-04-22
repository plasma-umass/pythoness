import pythoness
from typing import List, Optional

class Solution:
    
    def distanceSum(self, m: int, n: int, k: int) -> int:
        """
        Calculate the sum of Manhattan distances between all pairs of k identical pieces placed on an m × n grid. 
        Return the result for all valid arrangements of the pieces, ensuring only one piece per cell, and the result modulo 10^9 + 7. 
        The function adheres to constraints: 1 <= m, n <= 10^5, 2 <= m * n <= 10^5, 2 <= k <= m * n.
        """
        MOD = 10 ** 9 + 7
        # Initialize variables
        row_dist_sum = 0
        col_dist_sum = 0
        # Calculate total distance for rows using inclusion-exclusion principle
        for i in range(m):
            row_dist_sum += k * (k - 1) // 2 * (2 * i + 1 - m) % MOD
            row_dist_sum %= MOD
        # Calculate total distance for columns using inclusion-exclusion principle
        for j in range(n):
            col_dist_sum += k * (k - 1) // 2 * (2 * j + 1 - n) % MOD
            col_dist_sum %= MOD
        # Return the total sum of horizontal and vertical contributions
        total_distance_sum = (row_dist_sum + col_dist_sum) % MOD
        return total_distance_sum