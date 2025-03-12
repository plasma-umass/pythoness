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
    import re
    # Compile the pattern with the regex for full match '^...$'
    pattern = re.compile(f'^{p}$')
    # Use fullmatch which checks if the whole string matches the pattern
    match = pattern.fullmatch(s)
    # Return True if a match is found, otherwise return False
    return match is not None
isMatch(s='aa', p='a')