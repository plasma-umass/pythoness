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
    n = len(row) // 2  # The number of couples
    swaps = 0
    # Create a dictionary to map each person's position
    pos = {person: i for (i, person) in enumerate(row)}
    for i in range(n):
        first = row[2 * i]
        # Determine the expected second person of the couple
        if first % 2 == 0:
            partner = first + 1
        else:
            partner = first - 1
        # If the partner is not sitting next to the first person
        if row[2 * i + 1] != partner:
            # Find current position of the partner
            partner_pos = pos[partner]
            # Swap partner with the person sitting next to "first"
            (row[partner_pos], row[2 * i + 1]) = (row[2 * i + 1], row[partner_pos])
            # Update the positions in the dictionary
            (pos[row[partner_pos]], pos[row[2 * i + 1]]) = (partner_pos, 2 * i + 1)
            swaps += 1
    return swaps
minSwapsCouples(row=[0, 2, 1, 3])