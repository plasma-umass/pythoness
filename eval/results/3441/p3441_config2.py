import pythoness
from typing import List, Optional

@pythoness.spec(
    """Convert a given string caption into a 'good caption' where each character appears in groups of at least 3 consecutive occurrences. Utilize operations to change any character to its adjacent in the alphabet, aiming for the minimum number of changes. Return the lexicographically smallest possible good caption or an empty string if conversion is impossible.

Constraints:
- 1 <= caption.length <= 5 * 10^4
- The string consists only of lowercase English letters.""",
    tests=["""minCostGoodCaption(**{'caption': 'aazz'}) == 'aaaa'""", """minCostGoodCaption(**{'caption': 'abcdef'}) == 'bbbeee'""", """minCostGoodCaption(**{'caption': 'iiiiiii'}) == 'iiiiiii'""", """minCostGoodCaption(**{'caption': 'xyz'}) == 'yyy'""", """minCostGoodCaption(**{'caption': 'ppppqqqrrr'}) == 'ppppqqqrrr'""", """minCostGoodCaption(**{'caption': 'mmmmnn'}) == 'mmmnnn'""", """minCostGoodCaption(**{'caption': 'qqqqqq'}) == 'qqqqqq'""", """minCostGoodCaption(**{'caption': 'tttuuu'}) == 'tttuuu'""", """minCostGoodCaption(**{'caption': 'llmkp'}) == 'lllll'""", """minCostGoodCaption(**{'caption': ''}) == ''"""],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def minCostGoodCaption(caption: str) -> str:
    """"""

minCostGoodCaption(**{'caption': 'aazz'}) 