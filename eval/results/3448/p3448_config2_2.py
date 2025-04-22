import pythoness
from typing import List, Optional

@pythoness.spec(
    """Counts the substrings of a digit string divisible by their non-zero last digit.
Given a string `s` of digits, this function returns how many of its substrings can be divided by their last non-zero digit.
Constraints: 1 <= len(s) <= 10^5, s contains digits only.""",
    tests=["""countSubstrings(**{'s': '0'}) == '0'""", """countSubstrings(**{'s': '105'}) == '4'""", """countSubstrings(**{'s': '9999999999999999999999999'}) == '325'""", """countSubstrings(**{'s': '1234567890'}) == '20'""", """countSubstrings(**{'s': '888888'}) == '21'""", """countSubstrings(**{'s': '1000000000000000000000000'}) == '1'""", """countSubstrings(**{'s': '0'}) == '0'""", """countSubstrings(**{'s': '2000200020002'}) == '28'""", """countSubstrings(**{'s': '123456789012345678901234567890'}) == '205'""", """countSubstrings(**{'s': '33333333'}) == '36'"""],
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