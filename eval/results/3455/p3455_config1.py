import pythoness
from typing import List, Optional

@pythoness.spec(
    """Find the length of the shortest substring in a given string `s` that matches a pattern `p`, where `p` contains exactly two '*' characters, which can match any sequence of zero or more characters. Return the length of the shortest matching substring or -1 if no such substring exists. The empty substring is considered valid.""",
    tests=[],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def shortestMatchingSubstring(s: str, p: str) -> int:
    """"""

shortestMatchingSubstring(**{'s': 'aaaabcdef', 'p': '*b*'}) 