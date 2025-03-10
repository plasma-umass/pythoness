import pythoness
from typing import List

@pythoness.spec(
    """The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
Given an integer n, return the number of distinct solutions to the n-queens puzzle.
 
Constraints:

1 <= n <= 9""",
    tests=['totalNQueens(n = 4) == 2'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def totalNQueens(n: int) -> int:
    """"""

totalNQueens()