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
    k = len(s)
    num_digits = len(digits)
    count = 0
    # Count numbers with fewer digits than n
    for i in range(1, k):
        count += num_digits ** i
    # Count numbers with the same length as n
    for i in range(k):
        has_same_prefix = False
        for d in digits:
            if d < s[i]:
                count += num_digits ** (k - i - 1)
            elif d == s[i]:
                has_same_prefix = True
                break
        if not has_same_prefix:
            return count
    return count + 1
atMostNGivenDigitSet(digits=['1', '3', '5', '7'], n=100)