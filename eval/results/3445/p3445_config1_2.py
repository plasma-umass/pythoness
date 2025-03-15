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
    max_diff = -1
    n = len(s)
    # Function to calculate odd and even frequency of characters in a substring

    def calculate_frequency(subs):
        from collections import Counter
        counter = Counter(subs)
        odd_freq = {char: freq for (char, freq) in counter.items() if freq % 2 == 1}
        even_freq = {char: freq for (char, freq) in counter.items() if freq % 2 == 0}
        return (odd_freq, even_freq)
    for i in range(n):
        for j in range(i + k, n + 1):
            subs = s[i:j]
            (odd_freq, even_freq) = calculate_frequency(subs)
            if odd_freq and even_freq:
                max_odd = max(odd_freq.values())
                min_even = min(even_freq.values())
                max_diff = max(max_diff, max_odd - min_even)
    return max_diff
maxDifference(s='12233', k=4)