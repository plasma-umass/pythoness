import pythoness
from typing import List, Optional

class Solution:
    
    def generateString(self, str1: str, str2: str) -> str:
        """
        Generate the lexicographically smallest string from str1 and str2 given specific matching conditions. For
        each index in str1, if str1[i] is 'T', the substring of length m starting at that index must match str2, 
        otherwise, it must not match. If generating such a string is not possible, return an empty string.
        """
        m = len(str2)
        n = len(str1)
        result = []
        for i in range(n):
            if str1[i] == 'T':
                if i + m > n or str1[i:i + m] != 'T' * m:
                    return ''
                result.append(str2)
                i += m - 1
            else:
                if i + m <= n and str1[i:i + m] == 'T' * m:
                    return ''
                result.append('a')
        return ''.join(result)