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
    n = len(s)
    max_diff = float('-inf')
    # Iterate over all substrings of length >= k
    for start in range(n):
        count = [0] * 5
        odd_frequencies = []
        even_frequencies = []
        for end in range(start, n):
            count[int(s[end])] += 1
            length = end - start + 1
            # Check if the current substring has at least length k
            if length >= k:
                odd_frequencies.clear()
                even_frequencies.clear()
                # Determine frequencies of odd and even counts
                for i in range(5):
                    if count[i] > 0:
                        if count[i] % 2 == 0:
                            even_frequencies.append(count[i])
                        else:
                            odd_frequencies.append(count[i])
                if odd_frequencies and even_frequencies:
                    max_odd = max(odd_frequencies)
                    min_even = min(even_frequencies)
                    max_diff = max(max_diff, max_odd - min_even)
    return max_diff if max_diff != float('-inf') else -1
maxDifference(s='12233', k=4)