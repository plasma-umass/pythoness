import pythoness
from typing import List, Optional

def minSwapsCouples(row: List[int]) -> int:
    """
    There are n couples sitting in 2n seats arranged in a row and want to hold hands.
    The people and seats are represented by an integer array row where row[i] is the ID of the person sitting in the i^th seat. The couples are numbered in order, the first couple being (0, 1), the second couple being (2, 3), and so on with the last couple being (2n - 2, 2n - 1).
    Return the minimum number of swaps so that every couple is sitting side by side. A swap consists of choosing any two people, then they stand up and switch seats.

    Constraints:

    2n == row.length
    2 <= n <= 30
    n is even.
    0 <= row[i] < 2n
    All the elements of row are unique.
    """
    n = len(row) // 2
    # Create a position map where key is person and value is the position
    pos = {person: i for (i, person) in enumerate(row)}
    swaps = 0
    for i in range(n):
        first = row[2 * i]  # The first person in the couple
        second = first ^ 1  # The couple, either first+1 if first is even, or first-1 if odd
        # Check if this couple is already seated together
        if row[2 * i + 1] != second:
            swaps += 1
            # Find the position of the person that needs to swap with
            second_pos = pos[second]
            # Swap the second person in the current pair with the person at second_pos
            (row[2 * i + 1], row[second_pos]) = (row[second_pos], row[2 * i + 1])
            # Update their positions in the position map
            pos[row[second_pos]] = second_pos
            pos[row[2 * i + 1]] = 2 * i + 1
    return swaps
minSwapsCouples(row=[0, 2, 1, 3])