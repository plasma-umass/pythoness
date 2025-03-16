import pythoness
from typing import List, Optional
from typing import List

def solveNQueens(n: int) -> List[List[str]]:
    """
    The n-queens puzzle is the problem of placing n queens on an n x n chessboard 
    such that no two queens attack each other.
    Given an integer n, return all distinct solutions to the n-queens puzzle. You may 
    return the answer in any order. Each solution contains a distinct board configuration 
    of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, 
    respectively.

    Constraints:
    1 <= n <= 9
    """

    def backtrack(row: int) -> None:
        if row == n:
            result.append([''.join(row) for row in board])
            return
        for col in range(n):
            if not columns[col] and (not diagonals1[row + col]) and (not diagonals2[row - col]):
                board[row][col] = 'Q'
                columns[col] = diagonals1[row + col] = diagonals2[row - col] = True
                backtrack(row + 1)
                board[row][col] = '.'
                columns[col] = diagonals1[row + col] = diagonals2[row - col] = False
    result = []
    board = [['.'] * n for _ in range(n)]
    columns = [False] * n
    diagonals1 = [False] * (2 * n - 1)
    diagonals2 = [False] * (2 * n - 1)
    backtrack(0)
    return result
solveNQueens(n=4)