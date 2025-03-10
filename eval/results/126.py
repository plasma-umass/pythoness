import pythoness
from typing import List

@pythoness.spec(
    """A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].
 
Constraints:

1 <= beginWord.length <= 5
endWord.length == beginWord.length
1 <= wordList.length <= 500
wordList[i].length == beginWord.length
beginWord, endWord, and wordList[i] consist of lowercase English letters.
beginWord != endWord
All the words in wordList are unique.
The sum of all shortest transformation sequences does not exceed 10^5.""",
    tests=['findLadders(beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]) == [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]', 'findLadders(beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]) == []'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def findLadders(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    """"""

findLadders()