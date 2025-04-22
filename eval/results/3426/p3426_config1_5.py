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
        # Helper function to calculate combination nC2 which is n * (n - 1) // 2
    
        def combination2(n):
            return n * (n - 1) // 2
        # Precompute the sum of numbers from 0 to m-1 and 0 to n-1
        row_sum = [i * (m - i) * n % MOD for i in range(m)]
        col_sum = [j * (n - j) * m % MOD for j in range(n)]
        total_distance = 0
        for rk in range(min(k, m)):
            if k - rk < n:
                c = combination2(k)
                for r in range(rk + 1):
                    for c in range(k - rk):
                        # Add Row distances
                        total_distance += row_sum[r]
                        total_distance %= MOD
                        # Add Column distances
                        total_distance += col_sum[c]
                        total_distance %= MOD
        return total_distance