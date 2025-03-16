import pythoness
from typing import List, Optional

def findIntegers(n: int) -> int:
    """
    Given a positive integer n, return the number of the integers in the range [0, n] whose binary representations do not contain consecutive ones.

    Constraints:

    1 <= n <= 10^9
    """
    # Pre-compute fibonacci numbers
    fib = [0] * 31
    fib[0] = 1
    fib[1] = 2
    for i in range(2, 31):
        fib[i] = fib[i - 1] + fib[i - 2]
    last_bit = 0
    result = 0
    k = 30
    while k >= 0:
        if n & 1 << k != 0:
            result += fib[k]
            if last_bit == 1:
                return result
            last_bit = 1
        else:
            last_bit = 0
        k -= 1
    return result + 1
findIntegers(n=5)