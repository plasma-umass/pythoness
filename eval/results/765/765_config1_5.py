import pythoness
from typing import List, Optional

@pythoness.spec(
    """There are n couples sitting in 2n seats arranged in a row and want to hold hands.
The people and seats are represented by an integer array row where row[i] is the ID of the person sitting in the i^th seat. The couples are numbered in order, the first couple being (0, 1), the second couple being (2, 3), and so on with the last couple being (2n - 2, 2n - 1).
Return the minimum number of swaps so that every couple is sitting side by side. A swap consists of choosing any two people, then they stand up and switch seats.
 
Constraints:

2n == row.length
2 <= n <= 30
n is even.
0 <= row[i] < 2n
All the elements of row are unique.""",
    tests=['minSwapsCouples(row = [0,2,1,3]) == 1', 'minSwapsCouples(row = [3,2,0,1]) == 0'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minSwapsCouples(row: List[int]) -> int:
    """"""

minSwapsCouples(row = [0,2,1,3]) 