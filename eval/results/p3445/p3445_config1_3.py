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

    def is_valid(sub_freq):
        odd_exists = any((f % 2 == 1 for f in sub_freq.values()))
        even_exists = any((f % 2 == 0 for f in sub_freq.values()))
        return odd_exists and even_exists
    max_diff = -1
    n = len(s)
    # Slide over all possible starting points
    for start in range(n):
        counter = Counter()
        for end in range(start, n):
            counter[s[end]] += 1
            if end - start + 1 >= k:
                if is_valid(counter):
                    max_freq = max((freq for (char, freq) in counter.items() if freq % 2 == 1))
                    min_freq = min((freq for (char, freq) in counter.items() if freq % 2 == 0))
                    max_diff = max(max_diff, max_freq - min_freq)
    return max_diff
maxDifference(s='12233', k=4)