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
    if not s or not words or (not words[0]):
        return []
    word_length = len(words[0])
    total_words = len(words)
    total_length = word_length * total_words
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    result = []
    for i in range(word_length):
        left = i
        current_count = {}
        count = 0
        for j in range(i, len(s) - word_length + 1, word_length):
            sub = s[j:j + word_length]
            if sub in word_count:
                current_count[sub] = current_count.get(sub, 0) + 1
                count += 1
                while current_count[sub] > word_count[sub]:
                    leftmost_word = s[left:left + word_length]
                    current_count[leftmost_word] -= 1
                    left += word_length
                    count -= 1
                if count == total_words:
                    result.append(left)
            else:
                current_count.clear()
                count = 0
                left = j + word_length
    return result
findSubstring(s='barfoothefoobarman', words=['foo', 'bar'])