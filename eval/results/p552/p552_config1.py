import pythoness
from typing import List, Optional

@pythoness.spec(
    """An attendance record for a student can be represented as a string where each character signifies whether the student was absent, late, or present on that day. The record only contains the following three characters:

'A': Absent.
'L': Late.
'P': Present.

Any student is eligible for an attendance award if they meet both of the following criteria:

The student was absent ('A') for strictly fewer than 2 days total.
The student was never late ('L') for 3 or more consecutive days.

Given an integer n, return the number of possible attendance records of length n that make a student eligible for an attendance award. The answer may be very large, so return it modulo 10^9 + 7.
 
Constraints:

1 <= n <= 10^5""",
    tests=['checkRecord(n = 2) == 8', 'checkRecord(n = 1) == 3', 'checkRecord(n = 10101) == 183236316'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def checkRecord(n: int) -> int:
    """"""

checkRecord(n = 2) 