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
    if not digits or n <= 0:
        return 0
    s = str(n)
    k = len(s)
    dp = [0] * (k + 1)
    dp[k] = 1
    for i in range(k - 1, -1, -1):
        for digit in digits:
            if digit < s[i]:
                dp[i] += len(digits) ** (k - i - 1)
            elif digit == s[i]:
                dp[i] += dp[i + 1]
    total = sum((len(digits) ** i for i in range(1, k)))
    total += dp[0]
    return total
atMostNGivenDigitSet(digits=['1', '3', '5', '7'], n=100)