import pythoness
from typing import List, Optional

def permute(n: int, k: int) -> List[int]:
    """
    Given two integers, n and k, an alternating permutation is a permutation of the first n positive integers such that no two adjacent elements are both odd or both even.
    Return the k-th alternating permutation sorted in lexicographical order. If there are fewer than k valid alternating permutations, return an empty list.

    Constraints:
    1 <= n <= 100
    1 <= k <= 10^15
    """
    import itertools
    from collections import deque
    from typing import List

    def is_alternating(perm):
        return all((perm[i] % 2 != perm[i + 1] % 2 for i in range(len(perm) - 1)))
    numbers = list(range(1, n + 1))
    alternating_perms = deque()
    for perm in itertools.permutations(numbers):
        if is_alternating(perm):
            alternating_perms.append(list(perm))
            if len(alternating_perms) == k:
                return alternating_perms[-1]
    return []
permute(n=4, k=6)