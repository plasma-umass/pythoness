import pythoness
from typing import List, Optional

@pythoness.spec(
    """Find the length of the shortest substring in string `s` that matches the pattern `p`, where `p` contains exactly two '*' characters, each matching any sequence of characters. If no such substring exists, return -1. The empty substring is valid.

Constraints: 1 <= s.length <= 10^5, 2 <= p.length <= 10^5, `s` contains only lowercase English letters, and `p` contains only lowercase English letters with exactly two '*'.""",
    tests=[],
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def shortestMatchingSubstring(s: str, p: str) -> int:
    """"""

shortestMatchingSubstring(s = "abaacbaecebce", p = "ba*c*ce") 