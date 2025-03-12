import pythoness
from typing import List, Optional

def generateString(str1: str, str2: str) -> str:
    """
    You are given two strings, str1 and str2, of lengths n and m, respectively.
    A string word of length n + m - 1 is defined to be generated by str1 and str2 if it satisfies the following conditions for each index 0 <= i <= n - 1:

    If str1[i] == 'T', the substring of word with size m starting at index i is equal to str2, i.e., word[i..(i + m - 1)] == str2.
    If str1[i] == 'F', the substring of word with size m starting at index i is not equal to str2, i.e., word[i..(i + m - 1)] != str2.

    Return the lexicographically smallest possible string that can be generated by str1 and str2. If no string can be generated, return an empty string "".

    Constraints:

    1 <= n == str1.length <= 10^4
    1 <= m == str2.length <= 500
    str1 consists only of 'T' or 'F'.
    str2 consists only of lowercase English characters.
    """
    n = len(str1)
    m = len(str2)
    # A helper function that verifies if the word is valid by conditions

    def is_valid(word):
        for i in range(n):
            segment = word[i:i + m]
            if str1[i] == 'T':
                if segment != str2:
                    return False
            elif str1[i] == 'F':
                if segment == str2:
                    return False
        return True
    # We attempt to build the lexically smallest word
    word = ['a'] * (n + m - 1)
    for i in range(n):
        if str1[i] == 'T':
            word[i:i + m] = str2
    for i in range(n):
        if str1[i] == 'F':
            if word[i:i + m] == list(str2):
                # Attempt to change the first character of the duplicate to make it non-equal
                for j in range(m):
                    if word[i + j] != 'z':
                        word[i + j] = chr(ord(word[i + j]) + 1)
                        break
    final_word = ''.join(word)
    return final_word if is_valid(final_word) else ''
generateString(str1='TFTF', str2='ab')