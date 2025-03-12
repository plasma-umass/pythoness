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
    # dp[i][j][k] represents the number of valid sequences of length i,
    # with j 'A's and ending 'L' streak of length k
    dp = [[[0] * 3 for _ in range(2)] for _ in range(n + 1)]
    dp[0][0][0] = 1  # Base case: one way to have a zero-length string
    for i in range(1, n + 1):
        # Ending with 'P'
        for j in range(2):
            for k in range(3):
                dp[i][j][0] = (dp[i][j][0] + dp[i - 1][j][k]) % MOD
        # Ending with 'A'
        for k in range(3):
            dp[i][1][0] = (dp[i][1][0] + dp[i - 1][0][k]) % MOD
        # Ending with 'L'
        for j in range(2):
            for k in range(1, 3):
                dp[i][j][k] = (dp[i][j][k] + dp[i - 1][j][k - 1]) % MOD
    result = 0
    for j in range(2):
        for k in range(3):
            result = (result + dp[n][j][k]) % MOD
    return result
checkRecord(n=2)