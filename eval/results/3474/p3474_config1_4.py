import pythoness
from typing import List, Optional

class Solution:
    
    def generateString(self, str1: str, str2: str) -> str:
        """
        Generate the lexicographically smallest string from str1 and str2 given specific matching conditions. For each index in str1, if str1[i] is 'T', the substring of length m starting at that index must match str2, otherwise, it must not match. If generating such a string is not possible, return an empty string.
        """
        m = len(str2)
        n = len(str1)
        result = []
        i = 0
        while i < n:
            if str1[i] == 'T':
                if i + m <= n and str1[i:i + m] == 'T' * m:
                    result.append(str2)
                    i += m
                else:
                    return ''
            else:
                possible_chars = [chr(c) for c in range(ord('a'), ord('z') + 1)]
                for char in possible_chars:
                    if str1[i] != 'T' and char != str2[0]:
                        result.append(char)
                        break
                i += 1
        return ''.join(result) if result else ''