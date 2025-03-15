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
    if n == 1:
        return 3  # "P", "L", "A"
    if n == 2:
        return 8  # "PP", "PL", "LP", "LL", "AP", "PA", "LA", "AL"
    # dp[i][j][k] will represent the number of valid sequences of length i
    # where j is the count of 'A's and k is the length of the current sequence of 'L's
    dp = [[[0, 0, 0], [0, 0, 0]] for _ in range(n + 1)]
    dp[0][0][0] = 1
    for i in range(1, n + 1):
        for j in range(2):  # 0 or 1 'A'
            for k in range(3):  # 0, 1, or 2 'L's
                # Add 'P': 
                dp[i][j][0] = (dp[i][j][0] + dp[i - 1][j][k]) % MOD
                # Add 'A', if j == 0:
                if j == 0:
                    dp[i][1][0] = (dp[i][1][0] + dp[i - 1][j][k]) % MOD
                # Add 'L', if k < 2:
                if k < 2:
                    dp[i][j][k + 1] = (dp[i][j][k + 1] + dp[i - 1][j][k]) % MOD
    total = 0
    for j in range(2):
        for k in range(3):
            total = (total + dp[n][j][k]) % MOD
    return total
checkRecord(n=2)