import pythoness
from typing import List

@pythoness.spec(
    """The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.
 
Constraints:

1 <= n <= 9""",
    tests=['solveNQueens(n = 4) == [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def solveNQueens(n: int) -> List[List[str]]:
    """"""

solveNQueens()