import pythoness
from typing import List, Optional

def solveNQueens(n: int) -> List[List[str]]:
    """
    The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two
    queens attack each other. Given an integer n, return all distinct solutions to the n-queens puzzle.
    You may return the answer in any order. Each solution contains a distinct board configuration of
    the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

    Constraints:

    1 <= n <= 9

    """
    from typing import List

    def is_not_under_attack(row: int, col: int) -> bool:
        # Check if placing a queen in (row, col) is safe
        return not (cols[col] or hills[row - col] or dales[row + col])

    def place_queen(row: int, col: int):
        # Place a queen in (row, col)
        queens.add((row, col))
        cols[col] = True
        hills[row - col] = True
        dales[row + col] = True

    def remove_queen(row: int, col: int):
        # Remove a queen from (row, col)
        queens.remove((row, col))
        cols[col] = False
        hills[row - col] = False
        dales[row + col] = False

    def add_solution() -> None:
        # Add the current board configuration to the output
        solution = []
        for (_, col) in sorted(queens):
            solution.append('.' * col + 'Q' + '.' * (n - col - 1))
        output.append(solution)

    def backtrack(row: int) -> None:
        # Try to place queen on every square in the current row
        for col in range(n):
            if is_not_under_attack(row, col):
                place_queen(row, col)
                if row + 1 == n:
                    add_solution()
                else:
                    backtrack(row + 1)
                remove_queen(row, col)
    cols = [False] * n  # Columns    
    hills = [False] * (2 * n - 1)  # Main diagonals (hill direction)
    dales = [False] * (2 * n - 1)  # Counter diagonals (dale direction)
    queens = set()  # Set of tuples of the positions of queens
    output = []
    backtrack(0)
    return output
solveNQueens(n=4)