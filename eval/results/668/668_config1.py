import pythoness
from typing import List, Optional

@pythoness.spec(
    """Nearly everyone has used the Multiplication Table. The multiplication table of size m x n is an integer matrix mat where mat[i][j] == i * j (1-indexed).
Given three integers m, n, and k, return the k^th smallest element in the m x n multiplication table.
 
Constraints:

1 <= m, n <= 3 * 10^4
1 <= k <= m * n""",
    tests=['findKthNumber(m = 3, n = 3, k = 5) == 3', 'findKthNumber(m = 2, n = 3, k = 6) == 6'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def findKthNumber(m: int, n: int, k: int) -> int:
    """"""

findKthNumber(m = 3, n = 3, k = 5) 