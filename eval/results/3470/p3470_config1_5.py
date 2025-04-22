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
        # Generate the first n positive integers
        nums = list(range(1, n + 1))
        # Function to check if a permutation is alternating
    
        def is_alternating(perm):
            for i in range(len(perm) - 1):
                if perm[i] % 2 == perm[i + 1] % 2:
                    return False
            return True
        # Generate all permutations and filter by alternating property
        alternating_perms = sorted(filter(is_alternating, permutations(nums)))
        # Check if k-th permutation exists
        if k - 1 < len(alternating_perms):
            return list(alternating_perms[k - 1])
        else:
            return []