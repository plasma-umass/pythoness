import pythoness
from typing import List, Optional

@pythoness.spec(
    """Generate the lexicographically smallest string from str1 and str2 given specific matching conditions. For each index in str1, if str1[i] is 'T', the substring of length m starting at that index must match str2, otherwise, it must not match. If generating such a string is not possible, return an empty string.""",
    tests=["""generateString(**{'str1': 'T', 'str2': 'a'}) == 'a'""", """generateString(**{'str1': 'F', 'str2': 'b'}) == 'a'""", """generateString(**{'str1': 'TFT', 'str2': 'xyz'}) == ''""", """generateString(**{'str1': 'FTFT', 'str2': 'ghi'}) == ''""", """generateString(**{'str1': 'TTTT', 'str2': 'mnop'}) == ''""", """generateString(**{'str1': 'TFTF', 'str2': 'uvwx'}) == ''""", """generateString(**{'str1': 'FTTFTF', 'str2': 'efg'}) == ''""", """generateString(**{'str1': 'FTFFT', 'str2': 'klmno'}) == ''""", """generateString(**{'str1': 'TFTFTFTF', 'str2': 'fghij'}) == ''""", """generateString(**{'str1': 'FTTFTTFT', 'str2': 'klmnop'}) == ''"""],
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def generateString(str1: str, str2: str) -> str:
    """"""

generateString(**{'str1': 'T', 'str2': 'a'}) 