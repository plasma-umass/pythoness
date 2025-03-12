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
    from itertools import permutations
    from typing import List
    # Generate all numbers from 1 to n
    numbers = list(range(1, n + 1))
    # Helper function to check if a permutation is alternating

    def is_alternating(perm):
        for i in range(len(perm) - 1):
            if perm[i] % 2 == perm[i + 1] % 2:
                return False
        return True
    # Generate all lexicographical permutations
    alternate_perms = []
    for perm in permutations(numbers):
        if is_alternating(perm):
            alternate_perms.append(perm)
    # Check if k-th permutation exists
    if len(alternate_perms) < k:
        return []
    # Return k-th permutation in lexicographical order
    return list(alternate_perms[k - 1])
permute(n=4, k=6)