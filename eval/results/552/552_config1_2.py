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
    if n == 1:
        return 3
    # P[n][T] will be the number of valid sequences of length n that end with a type T
    # A valid sequence has not more than 1 'A' and less than three consecutive 'L'
    P = [[0] * 6 for _ in range(n + 1)]
    # Initialization
    P[0][0] = 1  # ""
    P[1][0] = 1  # "P"
    P[1][1] = 1  # "L"
    P[1][2] = 0  # No "LL" can appear
    P[1][3] = 1  # "A"
    P[1][4] = 0  # No "AL"
    P[1][5] = 0  # "ALL", impossible initially
    for i in range(2, n + 1):
        # Ending with "P"
        P[i][0] = (P[i - 1][0] + P[i - 1][1] + P[i - 1][2]) % MOD
        # Ending with "L"
        P[i][1] = P[i - 1][0] % MOD
        P[i][2] = P[i - 1][1] % MOD
        # Ending with "A"
        P[i][3] = (P[i - 1][0] + P[i - 1][1] + P[i - 1][2] + P[i - 1][3] + P[i - 1][4] + P[i - 1][5]) % MOD
        # Ending with "LL" after 'A'
        P[i][4] = P[i - 1][3] % MOD
        # Ending with "LLL" after 'A', impossible state
        P[i][5] = P[i - 1][4] % MOD
    # Sum all valid sequences
    return (P[n][0] + P[n][1] + P[n][2] + P[n][3] + P[n][4] + P[n][5]) % MOD
checkRecord(n=2)