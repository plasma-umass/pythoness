import pythoness
from typing import List, Optional
from typing import List

def findSubstring(s: str, words: List[str]) -> List[int]:
    """
    You are given a string s and an array of strings words. All the strings of words are of the same length.
    A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.

    For example, if words = ["ab","cd","ef"], then "abcdef", "abefcd", "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated strings. "acdbef" is not a concatenated string because it is not the concatenation of any permutation of words.

    Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.

    Constraints:

    1 <= s.length <= 10^4
    1 <= words.length <= 5000
    1 <= words[i].length <= 30
    s and words[i] consist of lowercase English letters.
    """
    if not s or not words:
        return []
    word_length = len(words[0])
    total_words = len(words)
    total_length = word_length * total_words
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    indices = []
    for i in range(len(s) - total_length + 1):
        seen = {}
        for j in range(total_words):
            word_start = i + j * word_length
            word_end = word_start + word_length
            current_word = s[word_start:word_end]
            if current_word in word_count:
                seen[current_word] = seen.get(current_word, 0) + 1
                if seen[current_word] > word_count[current_word]:
                    break
            else:
                break
        else:
            indices.append(i)
    return indices
findSubstring(s='barfoothefoobarman', words=['foo', 'bar'])