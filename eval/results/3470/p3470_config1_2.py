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
        all_numbers = list(range(1, n + 1))
        valid_permutations = sorted((p for p in permutations(all_numbers) if is_alternating(p)))
        if k > len(valid_permutations) or k <= 0:
            return []
        return list(valid_permutations[k - 1])