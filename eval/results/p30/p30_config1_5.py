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
    word_count = len(words)
    total_words_length = word_length * word_count
    words_dict = {}
    # Count the occurrence of each word in words
    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    result_indices = []
    # Slide over s with a step of 1 to check for concatenated substrings
    for i in range(len(s) - total_words_length + 1):
        seen_words = {}
        j = 0
        # Check the substring starting at index i
        while j < word_count:
            word_index = i + j * word_length
            current_word = s[word_index:word_index + word_length]
            if current_word in words_dict:
                if current_word in seen_words:
                    seen_words[current_word] += 1
                else:
                    seen_words[current_word] = 1
                # If the current word is seen more times than it appears in words, break
                if seen_words[current_word] > words_dict[current_word]:
                    break
            else:
                break
            j += 1
        # If all words are matched
        if j == word_count:
            result_indices.append(i)
    return result_indices
findSubstring(s='barfoothefoobarman', words=['foo', 'bar'])