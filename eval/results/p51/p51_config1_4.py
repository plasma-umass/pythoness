import pythoness
from typing import List, Optional
from typing import List

def solveNQueens(n: int) -> List[List[str]]:
    """
    The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
    Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
    Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

    Constraints:

    1 <= n <= 9
    """

    def is_not_under_attack(row, col):
        return not (cols[col] or hills[row - col] or dales[row + col])

    def place_queen(row, col):
        queens[row] = col
        cols[col] = 1
        hills[row - col] = 1
        dales[row + col] = 1

    def remove_queen(row, col):
        queens[row] = 0
        cols[col] = 0
        hills[row - col] = 0
        dales[row + col] = 0

    def add_solution():
        solution = []
        for i in range(n):
            row = ['.'] * n
            row[queens[i]] = 'Q'
            solution.append(''.join(row))
        output.append(solution)

    def backtrack(row=0):
        for col in range(n):
            if is_not_under_attack(row, col):
                place_queen(row, col)
                if row + 1 == n:
                    add_solution()
                else:
                    backtrack(row + 1)
                remove_queen(row, col)
    cols = [0] * n
    hills = [0] * (2 * n - 1)
    dales = [0] * (2 * n - 1)
    queens = [0] * n
    output = []
    backtrack()
    return output
solveNQueens(n=4)