import pythoness
from typing import List, Optional

def hasSameDigits(s: str) -> bool:
    """
    You are given a string s consisting of digits. Perform the following operation repeatedly until the string has exactly two digits:

    For each pair of consecutive digits in s, starting from the first digit, calculate a new digit as the sum of the two digits modulo 10.
    Replace s with the sequence of newly calculated digits, maintaining the order in which they are computed.

    Return true if the final two digits in s are the same; otherwise, return false.

    Constraints:

    3 <= s.length <= 10^5
    s consists of only digits.
    """
    while len(s) > 2:
        new_s = []
        for i in range(len(s) - 1):
            new_digit = (int(s[i]) + int(s[i + 1])) % 10
            new_s.append(str(new_digit))
        s = ''.join(new_s)
    return s[0] == s[1]
hasSameDigits(s='3902')