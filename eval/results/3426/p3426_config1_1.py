import pythoness
from typing import List, Optional

class Solution:
    
    def distanceSum(self, m: int, n: int, k: int) -> int:
        """
        Calculate the sum of Manhattan distances between all pairs of k identical pieces
        placed on an m × n grid. Return the result for all valid arrangements of the
        pieces, ensuring only one piece per cell, and the result modulo 10^9 + 7. The
        function adheres to constraints: 1 <= m, n <= 10^5, 2 <= m * n <= 10^5, 2 <= k <= m * n.
        """
        MOD = 10 ** 9 + 7
        # Helper function to calculate the sum of distances in one dimension
    
        def dimension_distance(size):
            prefix_sum = [0] * (size + 1)
            for i in range(1, size + 1):
                prefix_sum[i] = prefix_sum[i - 1] + i
            total_distance = 0
            for i in range(1, size + 1):
                left_sum = prefix_sum[i - 1]
                right_sum = prefix_sum[size] - prefix_sum[i]
                total_distance += (right_sum - left_sum) * (size - i)
            return total_distance % MOD
        # Calculate the contribution of distances row-wise and column-wise
        total_distance_x = dimension_distance(m)
        total_distance_y = dimension_distance(n)
        # Calculate the number of ways to choose 2 out of k pieces
        num_pairs = k * (k - 1) // 2
        # Total sum of distances is the sum of x-distances and y-distances
        result = num_pairs * (total_distance_x + total_distance_y) % MOD
        return result