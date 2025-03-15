import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given two integers, n and k, an alternating permutation is a permutation of the first n positive integers such that no two adjacent elements are both odd or both even.
Return the k-th alternating permutation sorted in lexicographical order. If there are fewer than k valid alternating permutations, return an empty list.
 
Constraints:

1 <= n <= 100
1 <= k <= 10^15""",
    tests=['permute(n = 4, k = 6) == [3,4,1,2]', 'permute(n = 3, k = 2) == [3,2,1]', 'permute(n = 2, k = 3) == []'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def permute(n: int, k: int) -> List[int]:
    """"""

permute(n = 4, k = 6) 