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
                if i + m <= n and str1[i:i + m] != str2:
                    return ''  # cannot match when required
                result.append(str2)
                i += m  # skip over the matched portion
            else:
                for j in range(26):  # try each letter a-z
                    next_char = chr(ord('a') + j)
                    if i + m <= n and str1[i:i + m] == str2:
                        continue  # cannot use if it matches when it shouldn't
                    result.append(next_char)
                    break
                i += 1
        return ''.join(result)