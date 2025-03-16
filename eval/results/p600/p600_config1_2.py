import pythoness
from typing import List, Optional

def findIntegers(n: int) -> int:
    """
    Given a positive integer n, return the number of the integers in the range [0, n] whose binary representations do not contain consecutive ones.

    Constraints:

    1 <= n <= 10^9
    """
    # The problem can be approached using dynamic programming and the Fibonacci sequence.
    # The idea is similar to solving the Fibonacci sequence where the count of numbers
    # with no consecutive ones is determined using the previously computed values.
    # Precompute the Fibonacci numbers up to 31 since 2^30 > 10^9
    fib = [0] * 31
    fib[0] = 1
    fib[1] = 2
    for i in range(2, 31):
        fib[i] = fib[i - 1] + fib[i - 2]
    # Resulting count
    result = 0
    # Previous bit (used for checking consecutive ones)
    prev_bit = 0
    # Process each bit from the most significant to the least significant
    for i in range(30, -1, -1):
        if n & 1 << i:
            # If the bit is 1, add the Fibonacci number corresponding to the position
            result += fib[i]
            # Check if there are consecutive ones
            if prev_bit == 1:
                # If there is a consecutive one, break
                result -= 1
                break
            # Mark that we had a 1 here
            prev_bit = 1
        else:
            # If the bit is 0, reset the previous bit indicator
            prev_bit = 0
    # Add 1 for the number itself when all checks are clear
    return result + 1
findIntegers(n=5)