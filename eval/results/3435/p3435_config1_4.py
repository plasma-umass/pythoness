import pythoness
from typing import List, Optional

class Solution:
    
    def supersequences(self, words: List[str]) -> List[List[int]]:
        """
        Finds all shortest common supersequences (SCS) of an array of strings that are not permutations of each other and returns their frequency arrays. 
        An SCS is a minimal-length string containing each string in the input words as a subsequence. 
        The result is a 2D array where each sub-array represents the frequency of each lowercase English letter in a distinct SCS.
        """
        from itertools import permutations
        from collections import Counter, defaultdict
    
        def is_subsequence(s, word):
            it = iter(s)
            return all((char in it for char in word))
    
        def merge_strings(a, b):
            merged = []
            (i, j) = (0, 0)
            while i < len(a) and j < len(b):
                if a[i] == b[j]:
                    merged.append(a[i])
                    i += 1
                    j += 1
                else:
                    merged.append(a[i])
                    i += 1
            merged.extend(a[i:])
            merged.extend(b[j:])
            return ''.join(merged)
    
        def scs_of_two(a, b):
            min_scs = None
            for perm in permutations(b):
                candidate = merge_strings(a, ''.join(perm))
                if min_scs is None or len(candidate) < len(min_scs):
                    min_scs = candidate
            return min_scs
    
        def scs(words):
            if not words:
                return ''
            current = words[0]
            for word in words[1:]:
                current = scs_of_two(current, word)
            return current
        all_scs = set()
        for perm in permutations(words):
            candidate = scs(perm)
            if not any((Counter(candidate) == Counter(scs) for scs in all_scs)):
                all_scs.add(candidate)
        result = []
        for scs_str in all_scs:
            freq_array = [0] * 26
            for char in scs_str:
                freq_array[ord(char) - ord('a')] += 1
            result.append(freq_array)
        return result