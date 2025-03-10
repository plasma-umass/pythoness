import pythoness
from typing import List

@pythoness.spec(
    """There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.
You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.

Return the minimum number of candies you need to have to distribute the candies to the children.
 
Constraints:

n == ratings.length
1 <= n <= 2 * 10^4
0 <= ratings[i] <= 2 * 10^4""",
    tests=['candy(ratings = [1,0,2]) == 5', 'candy(ratings = [1,2,2]) == 4'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def candy(ratings: List[int]) -> int:
    """"""

candy()