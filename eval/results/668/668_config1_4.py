import pythoness
from typing import List, Optional

def findKthNumber(m: int, n: int, k: int) -> int:
    """
    Nearly everyone has used the Multiplication Table. The multiplication table of size m x n is an integer matrix mat where mat[i][j] == i * j (1-indexed).
    Given three integers m, n, and k, return the k^th smallest element in the m x n multiplication table.

    Constraints:

    1 <= m, n <= 3 * 10^4
    1 <= k <= m * n
    """

    def count_less_equal(x):
        count = 0
        for i in range(1, m + 1):
            count += min(n, x // i)
        return count
    (left, right) = (1, m * n)
    while left < right:
        mid = (left + right) // 2
        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid
    return left
findKthNumber(m=3, n=3, k=5)