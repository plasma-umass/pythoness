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
    
        def is_alternating(seq):
            return all((seq[i] % 2 != seq[i + 1] % 2 for i in range(len(seq) - 1)))
        # Generate all permutations of the first n positive integers
        all_perms = permutations(range(1, n + 1))
        # Filter permutations to keep only alternating ones
        alt_perms = sorted(filter(is_alternating, all_perms))
        # Return the k-th one if it exists
        if k - 1 < len(alt_perms):
            return list(alt_perms[k - 1])
        else:
            return []