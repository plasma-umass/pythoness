import pythoness
from typing import List, Optional

def maxDifference(s: str, k: int) -> int:
    """
    You are given a string s and an integer k. Your task is to find the maximum difference between the frequency of two characters, freq[a] - freq[b], in a substring subs of s, such that:

    subs has a size of at least k.
    Character a has an odd frequency in subs.
    Character b has an even frequency in subs.

    Return the maximum difference.
    Note that subs can contain more than 2 distinct characters.

    Constraints:

    3 <= s.length <= 3 * 10^4
    s consists only of digits '0' to '4'.
    The input is generated that at least one substring has a character with an even frequency and a character with an odd frequency.
    1 <= k <= s.length
    """
    from collections import defaultdict
    max_diff = -1  # Initialize the max difference to -1
    for start in range(len(s)):
        freq = defaultdict(int)  # Dictionary to store the frequencies of characters
        for end in range(start, len(s)):
            freq[s[end]] += 1
            if end - start + 1 >= k:  # Check if the substring size is at least k
                odd_freqs = [key for (key, value) in freq.items() if value % 2 != 0]
                even_freqs = [key for (key, value) in freq.items() if value % 2 == 0]
                if odd_freqs and even_freqs:  # If both conditions are satisfied
                    max_odd = max((freq[odd] for odd in odd_freqs))
                    min_even = min((freq[even] for even in even_freqs))
                    max_diff = max(max_diff, max_odd - min_even)
    return max_diff
maxDifference(s='12233', k=4)