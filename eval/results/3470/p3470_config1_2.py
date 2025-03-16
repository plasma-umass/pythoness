import pythoness
from typing import List, Optional
from itertools import permutations
from typing import List

def permute(n: int, k: int) -> List[int]:
    """
    Given two integers, n and k, an alternating permutation is a permutation of the first n positive integers such that no two adjacent elements are both odd or both even.
    Return the k-th alternating permutation sorted in lexicographical order. If there are fewer than k valid alternating permutations, return an empty list.

    Constraints:

    1 <= n <= 100
    1 <= k <= 10^15
    """
    # Generate all permutations of the first n positive integers
    all_perms = permutations(range(1, n + 1))
    # Filter out valid alternating permutations
    valid_perms = []
    for perm in all_perms:
        if all((perm[i] % 2 != perm[i + 1] % 2 for i in range(n - 1))):
            valid_perms.append(perm)
    # Sort them lexicographically
    valid_perms.sort()
    # Return the k-th permutation if it exists
    if k <= len(valid_perms):
        return list(valid_perms[k - 1])
    else:
        return []
permute(n=4, k=6)