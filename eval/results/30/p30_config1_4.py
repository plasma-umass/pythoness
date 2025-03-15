import pythoness
from typing import List, Optional

def findSubstring(s: str, words: List[str]) -> List[int]:
    """
    You are given a string s and an array of strings words. All the strings of words are of the same length.
    A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.

    For example, if words = ["ab","cd","ef"], then "abcdef", "abefcd", "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated strings.
    "acdbef" is not a concatenated string because it is not the concatenation of any permutation of words.

    Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.

    Constraints:

    1 <= s.length <= 10^4
    1 <= words.length <= 5000
    1 <= words[i].length <= 30
    s and words[i] consist of lowercase English letters.
    """
    from collections import Counter
    if not s or not words:
        return []
    word_length = len(words[0])
    word_count = len(words)
    total_length = word_length * word_count
    if len(s) < total_length:
        return []
    # Count the words
    word_map = Counter(words)
    result = []
    # Iterate over each possible starting point
    for i in range(word_length):
        left = i
        count = 0
        current_map = Counter()
        # Slide the window
        for j in range(i, len(s) - word_length + 1, word_length):
            word = s[j:j + word_length]
            if word in word_map:
                current_map[word] += 1
                count += 1
                while current_map[word] > word_map[word]:
                    left_word = s[left:left + word_length]
                    current_map[left_word] -= 1
                    count -= 1
                    left += word_length
                if count == word_count:
                    result.append(left)
            else:
                current_map.clear()
                count = 0
                left = j + word_length
    return result
findSubstring(s='barfoothefoobarman', words=['foo', 'bar'])