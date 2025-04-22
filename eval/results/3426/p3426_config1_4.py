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
    
        def comb(n, k):
            if k > n:
                return 0
            if k == 0 or k == n:
                return 1
            num = 1
            denom = 1
            for i in range(k):
                num = num * (n - i) % MOD
                denom = denom * (i + 1) % MOD
            return num * pow(denom, MOD - 2, MOD) % MOD
    
        def totalManhattanDistance(a, b):
            total = 0
            for x in range(a):
                total += x * (a - x) * b * b
            for y in range(b):
                total += y * (b - y) * a * a
            return total
        total_distance = totalManhattanDistance(m, n)
        res = comb(m * n, k) * total_distance // comb(m * n - 2, k - 2) % MOD
        return res