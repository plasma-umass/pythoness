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
    
        def is_subsequence(small, large):
            it = iter(large)
            return all((char in it for char in small))
    
        def scs_of_two(a, b):
            # Build the shortest common supersequence of two strings a and b
            (m, n) = (len(a), len(b))
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0:
                        dp[i][j] = j
                    elif j == 0:
                        dp[i][j] = i
                    elif a[i - 1] == b[j - 1]:
                        dp[i][j] = 1 + dp[i - 1][j - 1]
                    else:
                        dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
            lcs = []
            (i, j) = (m, n)
            while i > 0 and j > 0:
                if a[i - 1] == b[j - 1]:
                    lcs.append(a[i - 1])
                    i -= 1
                    j -= 1
                elif dp[i - 1][j] < dp[i][j - 1]:
                    lcs.append(a[i - 1])
                    i -= 1
                else:
                    lcs.append(b[j - 1])
                    j -= 1
            while i > 0:
                lcs.append(a[i - 1])
                i -= 1
            while j > 0:
                lcs.append(b[j - 1])
                j -= 1
            return ''.join(reversed(lcs))
    
        def generate_all_scs(words):
            result = set()
            for perm_words in permutations(words):
                current_scs = perm_words[0]
                for word in perm_words[1:]:
                    current_scs = scs_of_two(current_scs, word)
                result.add(current_scs)
            return list(result)
        scs_list = generate_all_scs(words)
        frequency_array_result = []
        for scs in scs_list:
            frequency_array_result.append([scs.count(chr(i + ord('a'))) for i in range(26)])
        return frequency_array_result