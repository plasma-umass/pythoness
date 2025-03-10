import pythoness
from typing import List

@pythoness.spec(
    """A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
 
Constraints:

1 <= beginWord.length <= 10
endWord.length == beginWord.length
1 <= wordList.length <= 5000
wordList[i].length == beginWord.length
beginWord, endWord, and wordList[i] consist of lowercase English letters.
beginWord != endWord
All the words in wordList are unique.""",
    tests=['ladderLength(beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]) == 5', 'ladderLength(beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]) == 0'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """"""

ladderLength()