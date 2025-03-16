import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given a 0-indexed 2D integer array flowers, where flowers[i] = [starti, endi] means the i^th flower will be in full bloom from starti to endi (inclusive). You are also given a 0-indexed integer array people of size n, where people[i] is the time that the i^th person will arrive to see the flowers.
Return an integer array answer of size n, where answer[i] is the number of flowers that are in full bloom when the i^th person arrives.
 
Constraints:

1 <= flowers.length <= 5 * 10^4
flowers[i].length == 2
1 <= starti <= endi <= 10^9
1 <= people.length <= 5 * 10^4
1 <= people[i] <= 10^9""",
    tests=['fullBloomFlowers(flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]) == [1,2,2,2]', 'fullBloomFlowers(flowers = [[1,10],[3,3]], people = [3,3,2]) == [2,2,1]'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def fullBloomFlowers(flowers: List[List[int]], people: List[int]) -> List[int]:
    """"""

fullBloomFlowers(flowers = [[1,6],[3,7],[9,12],[4,13]], people = [2,3,7,11]) 