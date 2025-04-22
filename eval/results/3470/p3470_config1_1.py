import pythoness
from typing import List, Optional

class Solution:
    
    def permute(self, n: int, k: int) -> List[int]:
        """
        Returns the k-th lexicographically sorted alternating permutation of the first n positive integers.
        An alternating permutation ensures no two adjacent elements are both odd or both even.
        If fewer than k valid permutations exist, returns an empty list.
        """
        from itertools import permutations
    
        def is_alternating(perm):
            return all((perm[i] % 2 != perm[i + 1] % 2 for i in range(len(perm) - 1)))
        all_permutations = permutations(range(1, n + 1))
        alternating_perms = [perm for perm in all_permutations if is_alternating(perm)]
        if k <= len(alternating_perms):
            return list(alternating_perms[k - 1])
        else:
            return []