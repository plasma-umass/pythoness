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

    def find_partner(x):
        return x + 1 if x % 2 == 0 else x - 1
    pos = {person: i for (i, person) in enumerate(row)}
    swaps = 0
    for i in range(0, len(row), 2):
        (first, second) = (row[i], row[i + 1])
        partner = find_partner(first)
        if second != partner:
            partner_pos = pos[partner]
            (row[i + 1], row[partner_pos]) = (row[partner_pos], row[i + 1])
            (pos[second], pos[partner]) = (pos[partner], pos[second])
            swaps += 1
    return swaps
minSwapsCouples(row=[0, 2, 1, 3])