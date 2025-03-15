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
    # Initialize the DP table with False
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    # Base case: empty string matches with empty pattern
    dp[0][0] = True
    # Deals with patterns with '*' that can match with an empty string
    for j in range(2, len(p) + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    # Start populating the table
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                # Characters match or pattern has '.', exact match
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                # Star case
                # Consider the character before '*'
                dp[i][j] = dp[i][j - 2] or (dp[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.'))
    return dp[len(s)][len(p)]
isMatch(s='aa', p='a')