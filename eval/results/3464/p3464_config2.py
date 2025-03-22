import pythoness
from typing import List, Optional

@pythoness.spec(
    """Given an integer side representing the edge length of a square on a Cartesian plane and a 2D integer array points of coordinates on the boundary of the square, this function selects k elements from points to maximize the minimum Manhattan distance between any two selected points. The Manhattan Distance is defined as the sum of the absolute differences of their Cartesian coordinates. The objective is to return the maximum possible minimum distance for the selected k points, considering constraints on the number of points and their uniqueness on the boundary.""",
    tests=[],
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def maxDistance(side: int, points: List[List[int]], k: int) -> int:
    """"""

maxDistance(side = 2, points = [[0,2],[2,0],[2,2],[0,0]], k = 4) 