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
    swaps = 0
    position = {num: i for (i, num) in enumerate(row)}
    for i in range(n):
        first_person = row[2 * i]
        second_person = first_person ^ 1
        if row[2 * i + 1] != second_person:
            swaps += 1
            second_person_index = position[second_person]
            (row[2 * i + 1], row[second_person_index]) = (row[second_person_index], row[2 * i + 1])
            position[row[second_person_index]] = second_person_index
            position[second_person] = 2 * i + 1
    return swaps
minSwapsCouples(row=[0, 2, 1, 3])