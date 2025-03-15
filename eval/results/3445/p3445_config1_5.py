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
    from collections import Counter
    max_diff = -1
    for i in range(len(s) - k + 1):  # iterate over all valid starting indices for substrings of length at least k
        for j in range(i + k, len(s) + 1):  # try all valid ending index for substring starting at i
            subs = s[i:j]
            freq = Counter(subs)
            odd_frequencies = {char: count for (char, count) in freq.items() if count % 2 == 1}
            even_frequencies = {char: count for (char, count) in freq.items() if count % 2 == 0}
            if not odd_frequencies or not even_frequencies:
                continue
            max_odd_freq = max(odd_frequencies.values())
            min_even_freq = min(even_frequencies.values())
            current_diff = max_odd_freq - min_even_freq
            max_diff = max(max_diff, current_diff)
    return max_diff
maxDifference(s='12233', k=4)