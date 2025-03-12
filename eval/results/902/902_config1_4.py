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
    n_str = str(n)
    n_length = len(n_str)
    digits_length = len(digits)
    count = 0
    # Count numbers with length less than n
    for i in range(1, n_length):
        count += digits_length ** i
    # Count numbers with the same length as n
    for i in range(n_length):
        has_same_num = False
        for digit in digits:
            if digit < n_str[i]:
                count += digits_length ** (n_length - i - 1)
            elif digit == n_str[i]:
                has_same_num = True
                break
        if not has_same_num:
            return count
    return count + 1
atMostNGivenDigitSet(digits=['1', '3', '5', '7'], n=100)