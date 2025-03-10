import pythoness
from typing import List

@pythoness.spec(
    """The set [1, 2, 3, ..., n] contains a total of n! unique permutations.
By listing and labeling all of the permutations in order, we get the following sequence for n = 3:

"123"
"132"
"213"
"231"
"312"
"321"

Given n and k, return the k^th permutation sequence.
 
Constraints:

1 <= n <= 9
1 <= k <= n!""",
    tests=[],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def getPermutation(n: int, k: int) -> str:
    """"""

getPermutation()