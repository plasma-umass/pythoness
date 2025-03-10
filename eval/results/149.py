import pythoness
from typing import List

@pythoness.spec(
    """Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.
 
Constraints:

1 <= points.length <= 300
points[i].length == 2
-10^4 <= xi, yi <= 10^4
All the points are unique.""",
    tests=[],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def maxPoints(points: List[List[int]]) -> int:
    """"""

maxPoints()