import pythoness
from typing import List, Optional

@pythoness.spec(
    """Repeatedly transform the string `s` by replacing each pair of consecutive digits 
with their sum modulo 10, reducing `s` to two digits. Return true if the final 
two digits are the same, otherwise return false.

Constraints: 3 <= s.length <= 10^5; `s` consists only of digits.""",
    tests=[],
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def hasSameDigits(s: str) -> bool:
    """"""

hasSameDigits(s = "3902") 