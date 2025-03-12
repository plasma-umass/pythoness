import pythoness
from typing import List, Optional

def longestCommonSubpath(n: int, paths: List[List[int]]) -> int:
    """
    There is a country of n cities numbered from 0 to n - 1. In this country, there is a road connecting every pair of cities.
    There are m friends numbered from 0 to m - 1 who are traveling through the country. Each one of them will take a path consisting of some cities. Each path is represented by an integer array that contains the visited cities in order. The path may contain a city more than once, but the same city will not be listed consecutively.
    Given an integer n and a 2D integer array paths where paths[i] is an integer array representing the path of the i^th friend, return the length of the longest common subpath that is shared by every friend's path, or 0 if there is no common subpath at all.
    A subpath of a path is a contiguous sequence of cities within that path.

    Constraints:

    1 <= n <= 10^5
    m == paths.length
    2 <= m <= 10^5
    sum(paths[i].length) <= 10^5
    0 <= paths[i][j] < n
    The same city is not listed multiple times consecutively in paths[i].
    """
    from collections import defaultdict
    # Helper function to determine if a common subpath of length 'length' exists

    def check(length: int) -> bool:
        base = 10 ** 5 + 1
        hash_set = None
        for path in paths:
            # Compute rolling hash for subpaths of the current length
            current_hash = 0
            base_pow = 1
            current_set = set()
            for i in range(len(path)):
                current_hash = current_hash * base + path[i]
                if i >= length:
                    current_hash -= path[i - length] * base_pow
                else:
                    base_pow *= base
                if i >= length - 1:
                    current_set.add(current_hash)
            if hash_set is None:
                hash_set = current_set
            else:
                hash_set &= current_set
            if not hash_set:
                return False
        return True
    (left, right) = (0, min((len(path) for path in paths)))
    result = 0
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result
longestCommonSubpath(n=5, paths=[[0, 1, 2, 3, 4], [2, 3, 4], [4, 0, 1, 2, 3]])