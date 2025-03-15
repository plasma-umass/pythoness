import pythoness
from typing import List, Optional

def numberOfArrays(s: str, k: int) -> int:
    """
    A program was supposed to print an array of integers. The program forgot to print whitespaces and the array is printed as a string of digits s and all we know is that all integers in the array were in the range [1, k] and there are no leading zeros in the array.
    Given the string s and the integer k, return the number of the possible arrays that can be printed as s using the mentioned program. Since the answer may be very large, return it modulo 10^9 + 7.

    Constraints:
    1 <= s.length <= 10^5
    s consists of only digits and does not contain leading zeros.
    1 <= k <= 10^9
    """
    MOD = 10 ** 9 + 7
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(i):
            if s[j] == '0':
                continue
            num = int(s[j:i])
            if num > k:
                break
            dp[i] = (dp[i] + dp[j]) % MOD
    return dp[n]
numberOfArrays(s='1000', k=10000)