import pythoness
from typing import List, Optional

def findIntegers(n: int) -> int:
    """
    Given a positive integer n, return the number of the integers in the range [0, n] whose binary representations do not contain consecutive ones.

    Constraints:

    1 <= n <= 10^9
    """
    # Precompute Fibonacci numbers up to 31 (since we only need binary positions up to 31 for n <= 10^9)
    fib = [1, 2]
    for i in range(2, 32):
        fib.append(fib[-1] + fib[-2])
    # To count valid integers using the Fibonacci representation
    prev_bit = 0
    result = 0
    bit_index = 30  # Start from the highest bit position where n can be up to 2^30
    while bit_index >= 0:
        # Check if the bit at bit_index is set in n
        if n & 1 << bit_index != 0:
            result += fib[bit_index]
            if prev_bit == 1:
                # If two consecutive 1s found, terminate
                result -= 1
                break
            prev_bit = 1  # Mark current bit as 1
        else:
            prev_bit = 0  # Mark current bit as 0
        bit_index -= 1
    return result + 1  # Include n itself if it's a valid number
findIntegers(n=5)