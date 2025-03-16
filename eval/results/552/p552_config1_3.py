import pythoness
from typing import List, Optional

def checkRecord(n: int) -> int:
    """
    An attendance record for a student can be represented as a string where each character signifies whether the student was absent, late, or present on that day. The record only contains the following three characters:

    'A': Absent.
    'L': Late.
    'P': Present.

    Any student is eligible for an attendance award if they meet both of the following criteria:

    The student was absent ('A') for strictly fewer than 2 days total.
    The student was never late ('L') for 3 or more consecutive days.

    Given an integer n, return the number of possible attendance records of length n that make a student eligible for an attendance award. The answer may be very large, so return it modulo 10^9 + 7.

    Constraints:

    1 <= n <= 10^5
    """
    MOD = 10 ** 9 + 7
    # Initialize the dp arrays
    dp_P = [0] * (n + 1)
    dp_PL = [0] * (n + 1)
    dp_PLL = [0] * (n + 1)
    # Base cases
    dp_P[0] = 1
    dp_PL[0] = 0
    dp_PLL[0] = 0
    # Fill dp arrays
    for i in range(1, n + 1):
        dp_P[i] = (dp_P[i - 1] + dp_PL[i - 1] + dp_PLL[i - 1]) % MOD  # Ending with P
        dp_PL[i] = dp_P[i - 1] % MOD  # Ending with L
        dp_PLL[i] = dp_PL[i - 1] % MOD  # Ending with LL
    # Total sequences without an A
    total_without_A = (dp_P[n] + dp_PL[n] + dp_PLL[n]) % MOD
    # Calculate total with one 'A' being inserted at each position
    total_with_A = total_without_A  # Already calculated for 'A' at the start
    for i in range(n):
        total_with_A += (dp_P[i] + dp_PL[i] + dp_PLL[i]) * (dp_P[n - i - 1] + dp_PL[n - i - 1] + dp_PLL[n - i - 1])
        total_with_A %= MOD
    return total_with_A
checkRecord(n=2)