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

    def is_alternating(seq):
        # Check if sequence is alternating between odd and even
        for i in range(len(seq) - 1):
            if seq[i] % 2 == seq[i + 1] % 2:
                return False
        return True
    numbers = list(range(1, n + 1))
    count = 0
    # Generate all permutations and check for alternating property
    for perm in permutations(numbers):
        if is_alternating(perm):
            count += 1
            if count == k:
                return list(perm)
    # If fewer than k permutations, return an empty list
    return []
permute(n=4, k=6)