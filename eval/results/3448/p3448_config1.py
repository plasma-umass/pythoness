import pythoness
from typing import List, Optional

@pythoness.spec(
    """Counts the substrings of a digit string divisible by their non-zero last digit.
Given a string `s` of digits, this function returns how many of its substrings can be divided by their last non-zero digit.
Constraints: 1 <= len(s) <= 10^5, s contains digits only.""",
    tests=[],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def countSubstrings(s: str) -> int:
    """"""

countSubstrings(**{'s': '0'}) 