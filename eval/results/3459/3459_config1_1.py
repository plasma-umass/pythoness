import pythoness
from typing import List, Optional


def lenOfVDiagonal(grid: List[List[int]]) -> int:
    """
    You are given a 2D integer matrix grid of size n x m, where each element is either 0, 1, or 2.
    A V-shaped diagonal segment is defined as:

    The segment starts with 1.
    The subsequent elements follow this infinite sequence: 2, 0, 2, 0, ....
    The segment:

    Starts along a diagonal direction (top-left to bottom-right, bottom-right to top-left, top-right to bottom-left, or bottom-left to top-right).
    Continues the sequence in the same diagonal direction.
    Makes at most one clockwise 90-degree turn to another diagonal direction while maintaining the sequence.

    Return the length of the longest V-shaped diagonal segment. If no valid segment exists, return 0.

    Constraints:

    n == grid.length
    m == grid[i].length
    1 <= n, m <= 500
    grid[i][j] is either 0, 1 or 2.
    """
    from typing import List

    def is_valid_turn(current_direction, new_direction):
        # Allowable turns: 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 0
        return (current_direction + 1) % 4 == new_direction

    n = len(grid)
    m = len(grid[0]) if n > 0 else 0
    # Directions: (dy, dx)
    # 0: top-left to bottom-right
    # 1: top-right to bottom-left
    # 2: bottom-right to top-left
    # 3: bottom-left to top-right
    directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    max_length = 0

    def dfs(row, col, direction_idx, current_length, sequence_idx, turns_used):
        nonlocal max_length
        # Update max_length if current path is longer
        if current_length > max_length:
            max_length = current_length
        # Continue in the current direction
        (dy, dx) = directions[direction_idx]
        (new_row, new_col) = (row + dy, col + dx)
        if (
            0 <= new_row < n
            and 0 <= new_col < m
            and (grid[new_row][new_col] == sequence[sequence_idx])
        ):
            dfs(
                new_row,
                new_col,
                direction_idx,
                current_length + 1,
                (sequence_idx + 1) % 2,
                turns_used,
            )
        # Try to turn clockwise to a new valid direction if no turns have been used
        if turns_used == 0:
            for new_direction_idx in range(4):
                if new_direction_idx != direction_idx and is_valid_turn(
                    direction_idx, new_direction_idx
                ):
                    (dy, dx) = directions[new_direction_idx]
                    (new_row, new_col) = (row + dy, col + dx)
                    if (
                        0 <= new_row < n
                        and 0 <= new_col < m
                        and (grid[new_row][new_col] == sequence[sequence_idx])
                    ):
                        dfs(
                            new_row,
                            new_col,
                            new_direction_idx,
                            current_length + 1,
                            (sequence_idx + 1) % 2,
                            1,
                        )

    # The infinite sequence to follow
    sequence = [2, 0]
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                # Start new V-diagonal
                for d in range(4):
                    dfs(i, j, d, 1, 0, 0)  # Start at (i, j) with length 1
    return max_length


lenOfVDiagonal(
    grid=[
        [2, 2, 1, 2, 2],
        [2, 0, 2, 2, 0],
        [2, 0, 1, 1, 0],
        [1, 0, 2, 2, 2],
        [2, 0, 0, 2, 2],
    ]
)
