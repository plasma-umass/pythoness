import pythoness
from typing import List, Optional

@pythoness.spec(
    """Finds all shortest common supersequences (SCS) of an array of strings that are not permutations of each other and returns their frequency arrays. 
An SCS is a minimal-length string containing each string in the input words as a subsequence. 
The result is a 2D array where each sub-array represents the frequency of each lowercase English letter in a distinct SCS.""",
    tests=[],
    llm_unit=False,
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