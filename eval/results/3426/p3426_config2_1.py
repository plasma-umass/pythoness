import pythoness
from typing import List, Optional

@pythoness.spec(
    """Calculate the sum of Manhattan distances between all pairs of k identical pieces placed on an m × n grid. 
Return the result for all valid arrangements of the pieces, ensuring only one piece per cell, and the result modulo 10^9 + 7. 
The function adheres to constraints: 1 <= m, n <= 10^5, 2 <= m * n <= 10^5, 2 <= k <= m * n.""",
    tests=["""distanceSum(**{'m': 100, 'n': 1000, 'k': 200}) == '851542423'""", """distanceSum(**{'m': 500, 'n': 500, 'k': 10}) == '184808175'""", """distanceSum(**{'m': 100000, 'n': 1, 'k': 2}) == '665483338'""", """distanceSum(**{'m': 1, 'n': 100000, 'k': 2}) == '665483338'""", """distanceSum(**{'m': 333, 'n': 300, 'k': 99900}) == '880508186'""", """distanceSum(**{'m': 12345, 'n': 8, 'k': 10}) == '399014039'""", """distanceSum(**{'m': 400, 'n': 250, 'k': 3300}) == '50030707'""", """distanceSum(**{'m': 20, 'n': 5000, 'k': 100000}) == '582941438'""", """distanceSum(**{'m': 80, 'n': 80, 'k': 6400}) == '92095993'""", """distanceSum(**{'m': 300, 'n': 333, 'k': 90000}) == '658922961'"""],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def distanceSum(m: int, n: int, k: int) -> int:
    """"""

distanceSum(**{'m': 100, 'n': 1000, 'k': 200}) 