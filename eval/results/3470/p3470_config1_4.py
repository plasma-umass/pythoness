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
            return all(((perm[i] + perm[i + 1]) % 2 != 0 for i in range(len(perm) - 1)))
        all_numbers = list(range(1, n + 1))
        all_perms = permutations(all_numbers)
        valid_perms = (list(perm) for perm in all_perms if is_alternating(perm))
        sorted_valid_perms = sorted(valid_perms)
        if k <= len(sorted_valid_perms):
            return sorted_valid_perms[k - 1]
        else:
            return []