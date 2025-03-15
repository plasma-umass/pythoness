import pythoness
from typing import List, Optional
from itertools import permutations
from typing import List

def permute(n: int, k: int) -> List[int]:
    """
    Given two integers, n and k, an alternating permutation is a permutation of the first n positive integers
    such that no two adjacent elements are both odd or both even.
    Return the k-th alternating permutation sorted in lexicographical order. If there are fewer than k valid
    alternating permutations, return an empty list.

    Constraints:

    1 <= n <= 100
    1 <= k <= 10^15
    """

    def is_alternating(perm):
        for i in range(len(perm) - 1):
            if perm[i] % 2 == 0 and perm[i + 1] % 2 == 0 or (perm[i] % 2 == 1 and perm[i + 1] % 2 == 1):
                return False
        return True
    numbers = list(range(1, n + 1))
    alternating_perms = []
    for perm in permutations(numbers):
        if is_alternating(perm):
            alternating_perms.append(perm)
            if len(alternating_perms) == k:
                return list(perm)
    return []
permute(n=4, k=6)