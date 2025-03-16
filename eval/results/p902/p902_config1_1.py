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
    str_n = str(n)
    length_n = len(str_n)
    total_count = 0
    # Count numbers with fewer digits than n.
    for i in range(1, length_n):
        total_count += len(digits) ** i
    # Count numbers with the same number of digits.
    for i in range(length_n):
        smaller_digits_count = 0
        for d in digits:
            if d < str_n[i]:
                smaller_digits_count += 1
            elif d == str_n[i]:
                if i == length_n - 1:
                    total_count += 1
                break
        total_count += smaller_digits_count * len(digits) ** (length_n - i - 1)
        # If there's no current digit d in digits that matches str_n[i], break.
        if str_n[i] not in digits:
            break
    return total_count
atMostNGivenDigitSet(digits=['1', '3', '5', '7'], n=100)