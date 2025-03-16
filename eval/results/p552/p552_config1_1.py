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
    if n == 0:
        return 0
    # dp[i][j][k]:
    # i: number of days
    # j: number of 'A's
    # k: length of ending 'L's
    dp = [[[0] * 3 for _ in range(2)] for _ in range(n + 1)]
    dp[0][0][0] = 1
    for i in range(1, n + 1):
        for j in range(2):
            # Ending with 'P'
            dp[i][j][0] = (dp[i - 1][j][0] + dp[i - 1][j][1] + dp[i - 1][j][2]) % MOD
            # Ending with 'L'
            if j < 2:
                dp[i][j][1] = dp[i - 1][j][0] % MOD
                dp[i][j][2] = dp[i - 1][j][1] % MOD
            if j > 0:
                # Adding 'A'
                dp[i][j][0] = (dp[i][j][0] + dp[i - 1][j - 1][0] + dp[i - 1][j - 1][1] + dp[i - 1][j - 1][2]) % MOD
    return (dp[n][0][0] + dp[n][0][1] + dp[n][0][2] + dp[n][1][0] + dp[n][1][1] + dp[n][1][2]) % MOD
checkRecord(n=2)