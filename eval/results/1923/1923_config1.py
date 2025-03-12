import pythoness
from typing import List, Optional

@pythoness.spec(
    """There is a country of n cities numbered from 0 to n - 1. In this country, there is a road connecting every pair of cities.
There are m friends numbered from 0 to m - 1 who are traveling through the country. Each one of them will take a path consisting of some cities. Each path is represented by an integer array that contains the visited cities in order. The path may contain a city more than once, but the same city will not be listed consecutively.
Given an integer n and a 2D integer array paths where paths[i] is an integer array representing the path of the i^th friend, return the length of the longest common subpath that is shared by every friend's path, or 0 if there is no common subpath at all.
A subpath of a path is a contiguous sequence of cities within that path.
 
Constraints:

1 <= n <= 10^5
m == paths.length
2 <= m <= 10^5
sum(paths[i].length) <= 10^5
0 <= paths[i][j] < n
The same city is not listed multiple times consecutively in paths[i].""",
    tests=['longestCommonSubpath(n = 5, paths = [[0,1,2,3,4],[2,3,4],[4,0,1,2,3]]) == 2', 'longestCommonSubpath(n = 3, paths = [[0],[1],[2]]) == 0', 'longestCommonSubpath(n = 5, paths = [[0,1,2,3,4],[4,3,2,1,0]]) == 1'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def longestCommonSubpath(n: int, paths: List[List[int]]) -> int:
    """"""

longestCommonSubpath(n = 5, paths = [[0,1,2,3,4],[2,3,4],[4,0,1,2,3]]) 