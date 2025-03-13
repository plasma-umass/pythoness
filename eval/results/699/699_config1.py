import pythoness
from typing import List, Optional

@pythoness.spec(
    """There are several squares being dropped onto the X-axis of a 2D plane.
You are given a 2D integer array positions where positions[i] = [lefti, sideLengthi] represents the i^th square with a side length of sideLengthi that is dropped with its left edge aligned with X-coordinate lefti.
Each square is dropped one at a time from a height above any landed squares. It then falls downward (negative Y direction) until it either lands on the top side of another square or on the X-axis. A square brushing the left/right side of another square does not count as landing on it. Once it lands, it freezes in place and cannot be moved.
After each square is dropped, you must record the height of the current tallest stack of squares.
Return an integer array ans where ans[i] represents the height described above after dropping the i^th square.
 
Constraints:

1 <= positions.length <= 1000
1 <= lefti <= 10^8
1 <= sideLengthi <= 10^6""",
    tests=['fallingSquares(positions = [[1,2],[2,3],[6,1]]) == [2,5,5]', 'fallingSquares(positions = [[100,100],[200,100]]) == [100,100]'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def fallingSquares(positions: List[List[int]]) -> List[int]:
    """"""

fallingSquares(positions = [[1,2],[2,3],[6,1]]) 