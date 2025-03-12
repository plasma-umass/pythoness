import pythoness
from typing import List, Optional

def atMostNGivenDigitSet(digits: List[str], n: int) -> int:
    """
    Given an array of digits which is sorted in non-decreasing order. You can write numbers using each digits[i] as many times as we want. For example, if digits = ['1','3','5'], we may write numbers such as '13', '551', and '1351315'.
    Return the number of positive integers that can be generated that are less than or equal to a given integer n.

    Constraints:

    1 <= digits.length <= 9
    digits[i].length == 1
    digits[i] is a digit from '1' to '9'.
    All the values in digits are unique.
    digits is sorted in non-decreasing order.
    1 <= n <= 10^9
    """
    s = str(n)
    (m, d_len) = (len(s), len(digits))
    res = sum((d_len ** i for i in range(1, m)))
    for i in range(m):
        c = sum((x < s[i] for x in digits))
        res += c * d_len ** (m - i - 1)
        if s[i] not in digits:
            return res
    return res + 1
atMostNGivenDigitSet(digits=['1', '3', '5', '7'], n=100)