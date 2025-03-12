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
    word_len = len(words[0])
    total_len = word_len * len(words)
    word_count = {}
    result = []
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    for i in range(len(s) - total_len + 1):
        seen = {}
        for j in range(0, len(words)):
            next_word_index = i + j * word_len
            word = s[next_word_index:next_word_index + word_len]
            if word not in word_count:
                break
            if word in seen:
                seen[word] += 1
            else:
                seen[word] = 1
            if seen[word] > word_count[word]:
                break
            if j + 1 == len(words):
                result.append(i)
    return result
findSubstring(s='barfoothefoobarman', words=['foo', 'bar'])