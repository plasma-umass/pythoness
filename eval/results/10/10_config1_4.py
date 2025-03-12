import pythoness
from typing import List, Optional

def isMatch(s: str, p: str) -> bool:
    """
    Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

    '.' Matches any single character.    
    '*' Matches zero or more of the preceding element.

    The matching should cover the entire input string (not partial).

    Constraints:

    1 <= s.length <= 20
    1 <= p.length <= 20
    s contains only lowercase English letters.
    p contains only lowercase English letters, '.', and '*'.
    It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.
    """
    # Dynamic programming table
    table = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    table[0][0] = True  # Empty string matches empty pattern
    # Fill out first row for patterns like a*, a*b*, a*b*c*, etc.
    for j in range(2, len(p) + 1):
        if p[j - 1] == '*':
            table[0][j] = table[0][j - 2]
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '*':
                table[i][j] = table[i][j - 2] or (table[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.'))
            else:
                table[i][j] = table[i - 1][j - 1] and (s[i - 1] == p[j - 1] or p[j - 1] == '.')
    return table[len(s)][len(p)]
isMatch(s='aa', p='a')