import pythoness
from typing import List, Optional

def findIntegers(n: int) -> int:
    """
    Given a positive integer n, return the number of the integers in the range [0, n] whose binary representations do not contain consecutive ones.

    Constraints:

    1 <= n <= 10^9
    """
    # Precompute the Fibonacci numbers up to 31
    # as they represent the count of valid numbers for each bit length
    fib = [0] * 32
    (fib[0], fib[1]) = (1, 2)
    for i in range(2, 32):
        fib[i] = fib[i - 1] + fib[i - 2]
    # Result variable
    result = 0
    # Previous bit value
    prev_bit = 0
    # Parse through bits of n from the most significant to least
    for i in range(31, -1, -1):
        if n & 1 << i:
            # Add the number of valid integers with exactly i bits
            result += fib[i]
            # If there are two consecutive 1s, break the loop
            if prev_bit == 1:
                result -= 1
                break
            prev_bit = 1
        else:
            prev_bit = 0
    # Include n itself if no consecutive 1s were found
    return result + 1
findIntegers(n=5)