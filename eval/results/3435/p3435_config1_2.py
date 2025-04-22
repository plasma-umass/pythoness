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
    
        def is_subsequence(small, large):
            it = iter(large)
            return all((char in it for char in small))
    
        def scs_length(a, b):
            """ Returns length of the shortest common supersequence of strings a and b """
            (m, n) = (len(a), len(b))
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(m + 1):
                for j in range(n + 1):
                    if i == 0:
                        dp[i][j] = j
                    elif j == 0:
                        dp[i][j] = i
                    elif a[i - 1] == b[j - 1]:
                        dp[i][j] = dp[i - 1][j - 1] + 1
                    else:
                        dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)
            return dp[m][n]
    
        def get_frequencies(s):
            """ Returns frequency array of lowercase letters for string s """
            freq = [0] * 26
            for char in s:
                freq[ord(char) - ord('a')] += 1
            return freq
    
        def all_scs_combinations(word_list):
            """ Generates all shortest common supersequences for the given word list. """
            if not word_list:
                return []
            scss = set()
            for perm in permutations(word_list):
                candidate = perm[0]
                for word in perm[1:]:
                    l = len(candidate)
                    for i in range(l + 1):
                        if is_subsequence(word, candidate[i:] + word):
                            candidate = candidate[:i] + word + candidate[i:]
                            break
                scss.add(candidate)
            min_length = min((len(scs) for scs in scss))
            return [scs for scs in scss if len(scs) == min_length]
        unique_scss = all_scs_combinations(words)
        return [get_frequencies(scs) for scs in unique_scss]