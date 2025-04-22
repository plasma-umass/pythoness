import pythoness
from typing import List, Optional

@pythoness.spec(
    """Finds all shortest common supersequences (SCS) of an array of strings that are not permutations of each other and returns their frequency arrays. 
An SCS is a minimal-length string containing each string in the input words as a subsequence. 
The result is a 2D array where each sub-array represents the frequency of each lowercase English letter in a distinct SCS.""",
    tests=["""supersequences(**{'words': ['ax', 'xb', 'ay', 'by']}) == '[[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]'""", """supersequences(**{'words': ['ab', 'cd', 'ef', 'gh']}) == '[[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['xy', 'yx', 'xx', 'yy']}) == '[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0]]'""", """supersequences(**{'words': ['ab', 'bc']}) == '[[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['fg', 'gf']}) == '[[0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['lm', 'mn', 'no']}) == '[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['ba', 'bb', 'bc']}) == '[[1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['rs', 'st']}) == '[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['ek', 'ke']}) == '[[0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'""", """supersequences(**{'words': ['vw', 'wx', 'xy', 'yu']}) == '[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]]'"""],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def supersequences(words: List[str]) -> List[List[int]]:
    """"""

supersequences(**{'words': ['ax', 'xb', 'ay', 'by']}) 