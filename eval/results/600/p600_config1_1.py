import pythoness
from typing import List, Optional

def findIntegers(n: int) -> int:
    """
    Given a positive integer n, return the number of the integers in the range [0, n] whose binary representations do not contain consecutive ones.

    Constraints:

    1 <= n <= 10^9
    """
    # To solve the problem, we use dynamic programming. We create an array `dp` where `dp[i]`
    # is the number of binary strings of length `i` which do not contain consecutive 1s.
    # First two bases: 
    # dp[0] = 1 (empty string)
    # dp[1] = 2 ("0", "1")
    dp = [0] * 32
    (dp[0], dp[1]) = (1, 2)
    # Fill the dp array, which states the number of valid strings
    for i in range(2, 32):
        dp[i] = dp[i - 1] + dp[i - 2]
    result = 0
    prev_bit = 0
    # Check each bit position of n from most significant bit to least
    for i in range(31, -1, -1):
        # Check if the current bit in n is set (1)
        if n & 1 << i != 0:
            result += dp[i]
            if prev_bit == 1:
                # If there are consecutive 1s, break
                result -= 1
                break
            prev_bit = 1
        else:
            prev_bit = 0
    # Add 1 to include n itself if it's valid
    return result + 1
findIntegers(n=5)