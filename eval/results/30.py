import pythoness
from typing import List

@pythoness.spec(
    """You are given a string s and an array of strings words. All the strings of words are of the same length.
A concatenated string is a string that exactly contains all the strings of any permutation of words concatenated.

For example, if words = ["ab","cd","ef"], then "abcdef", "abefcd", "cdabef", "cdefab", "efabcd", and "efcdab" are all concatenated strings. "acdbef" is not a concatenated string because it is not the concatenation of any permutation of words.

Return an array of the starting indices of all the concatenated substrings in s. You can return the answer in any order.
 
Constraints:

1 <= s.length <= 10^4
1 <= words.length <= 5000
1 <= words[i].length <= 30
s and words[i] consist of lowercase English letters.""",
    tests=['findSubstring(s = "barfoothefoobarman", words = ["foo","bar"]) == [0,9]', 'findSubstring(s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]) == []', 'findSubstring(s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]) == [6,9,12]'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def findSubstring(s: str, words: List[str]) -> List[int]:
    """"""

findSubstring()