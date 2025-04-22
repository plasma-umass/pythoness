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
        from collections import Counter
    
        def is_subsequence(x, y):
            it = iter(y)
            return all((char in it for char in x))
    
        def scs(x, y):
            """Helper function to find the shortest common supersequence of two strings."""
            (m, n) = (len(x), len(y))
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0 or j == 0:
                        dp[i][j] = i + j
                    elif x[i - 1] == y[j - 1]:
                        dp[i][j] = 1 + dp[i - 1][j - 1]
                    else:
                        dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
            (i, j) = (m, n)
            result = []
            while i > 0 and j > 0:
                if x[i - 1] == y[j - 1]:
                    result.append(x[i - 1])
                    i -= 1
                    j -= 1
                elif dp[i - 1][j] < dp[i][j - 1]:
                    result.append(x[i - 1])
                    i -= 1
                else:
                    result.append(y[j - 1])
                    j -= 1
            while i > 0:
                result.append(x[i - 1])
                i -= 1
            while j > 0:
                result.append(y[j - 1])
                j -= 1
            return ''.join(result[::-1])
    
        def all_permutations(lst):
            """Generate sorted unique permutations to avoid duplicate SCS by permutations."""
            return set(permutations(sorted(lst)))
    
        def calculate_frequency(scs):
            """Helper function to calculate frequency of each lowercase letter in a string."""
            freq = [0] * 26
            for char in scs:
                if char.islower():
                    freq[ord(char) - ord('a')] += 1
            return freq
        scs_list = set()
        for perm in all_permutations(words):
            current_scs = perm[0]
            for word in perm[1:]:
                current_scs = scs(current_scs, word)
            scs_list.add(current_scs)
        # Filter out scs strings that are permutations of each other
        unique_scs = set()
        for scs_str in scs_list:
            if not any((is_subsequence(perm, scs_str) and is_subsequence(scs_str, perm) for perm in unique_scs)):
                unique_scs.add(scs_str)
        result = [calculate_frequency(s) for s in unique_scs]
        return result