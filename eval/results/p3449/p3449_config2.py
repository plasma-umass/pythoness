import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given an array points of size n and an integer m. There is another array gameScore of size n, where gameScore[i] represents the score achieved at the i^th game. Initially, gameScore[i] == 0 for all i.
You start at index -1, which is outside the array (before the first position at index 0). You can make at most m moves. In each move, you can either:

Increase the index by 1 and add points[i] to gameScore[i].
Decrease the index by 1 and add points[i] to gameScore[i].

Note that the index must always remain within the bounds of the array after the first move.
Return the maximum possible minimum value in gameScore after at most m moves.
 
Constraints:

2 <= n == points.length <= 5 * 10^4
1 <= points[i] <= 10^6
1 <= m <= 10^9""",
    tests=['maxScore(points = [2,4], m = 3) == 4', 'maxScore(points = [1,2,3], m = 5) == 2'],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def maxScore(points: List[int], m: int) -> int:
    """"""

maxScore(points = [2,4], m = 3) 