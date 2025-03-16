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
        for prev_row in range(row):
            if board[prev_row] == col or board[prev_row] - prev_row == col - row or board[prev_row] + prev_row == col + row:
                return False
        return True

    def place_queen(row):
        if row == n:
            solution = []
            for i in range(n):
                line = '.' * board[i] + 'Q' + '.' * (n - board[i] - 1)
                solution.append(line)
            solutions.append(solution)
        else:
            for col in range(n):
                if is_not_under_attack(row, col):
                    board[row] = col
                    place_queen(row + 1)
                    board[row] = -1
    board = [-1] * n
    solutions = []
    place_queen(0)
    return solutions
solveNQueens(n=4)