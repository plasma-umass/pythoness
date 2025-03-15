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
    # Using dynamic programming approach
    n = len(s)
    m = len(p)
    # dp[i][j] means whether s[:i] matches p[:j]
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    # Fill the dp array for empty string matching
    for j in range(1, m + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    # Fill the dp array for each character in s and p
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2] or ((p[j - 2] == '.' or p[j - 2] == s[i - 1]) and dp[i - 1][j])
    return dp[n][m]
isMatch(s='aa', p='a')