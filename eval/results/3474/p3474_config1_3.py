import pythoness
from typing import List, Optional

class Solution:
    
    def generateString(self, str1: str, str2: str) -> str:
        """
        Generate the lexicographically smallest string from str1 and str2 given specific matching conditions. For each index in str1, if str1[i] is 'T', the substring of length m starting at that index must match str2, otherwise, it must not match. If generating such a string is not possible, return an empty string.
        """
        m = len(str2)
        n = len(str1)
        if n - m < 0:
            return ''
        result = list(str1)
        i = 0
        while i <= n - m:
            if str1[i] == 'T':
                if str1[i:i + m] == str2:
                    i += m
                    continue
                else:
                    return ''
            i += 1
        for j in range(n - m + 1, n):
            if str1[j] == 'T':
                return ''
        for i in range(n):
            if result[i] == 'T':
                result[i] = 'A' if str2[0] != 'A' else 'B'
            else:
                min_char = 'A'
                if n - i >= m and str1[i:i + m] == 'T' * m:
                    for j in range(m):
                        min_char = min(min_char, str2[j])
                    result[i] = min_char
                    i += m - 1
                else:
                    result[i] = str1[i]
        return ''.join(result)