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
    
        def is_subsequence(x, y):
            it = iter(y)
            return all((c in it for c in x))
    
        def can_form_scs(candidate, words):
            return all((is_subsequence(word, candidate) for word in words))
    
        def get_letter_frequency(s):
            return [s.count(chr(i)) for i in range(ord('a'), ord('z') + 1)]
        # This is to keep track of distinct supersequences
        unique_supersequences = set()
        # Find possible permutations of words concatenated
        for perm in permutations(words):
            candidate = ''.join(perm)
            if can_form_scs(candidate, words):
                unique_supersequences.add(candidate)
        # Now we extract the letter frequencies for each unique supersequence
        frequency_list = []
        seen = set()
        for superseq in unique_supersequences:
            freq_array = tuple(get_letter_frequency(superseq))
            # Ensure we are not adding permutations by checking the frequency array
            if freq_array not in seen:
                seen.add(freq_array)
                frequency_list.append(list(freq_array))
        return frequency_list