import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given an array of digits which is sorted in non-decreasing order. You can write numbers using each digits[i] as many times as we want. For example, if digits = ['1','3','5'], we may write numbers such as '13', '551', and '1351315'.
Return the number of positive integers that can be generated that are less than or equal to a given integer n.
 
Constraints:

1 <= digits.length <= 9
digits[i].length == 1
digits[i] is a digit from '1' to '9'.
All the values in digits are unique.
digits is sorted in non-decreasing order.
1 <= n <= 10^9""",
    tests=['atMostNGivenDigitSet(digits = ["1","3","5","7"], n = 100) == 20', 'atMostNGivenDigitSet(digits = ["1","4","9"], n = 1000000000) == 29523', 'atMostNGivenDigitSet(digits = ["7"], n = 8) == 1'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def atMostNGivenDigitSet(digits: List[str], n: int) -> int:
    """"""

atMostNGivenDigitSet(digits = ["1","3","5","7"], n = 100) 