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

    def check(length: int) -> bool:
        """Helper function to check for common subpath of given length."""
        MOD = 2 ** 61 - 1
        base = 10 ** 5 + 7

        def compute_hash(path: List[int], length: int) -> int:
            """Compute the initial hash for the first 'length' length path."""
            h = 0
            for i in range(length):
                h = (h * base + path[i]) % MOD
            return h
        multiplier = pow(base, length, MOD)
        common_hashes = None
        for path in paths:
            current_hashes = set()
            h = compute_hash(path, length)
            current_hashes.add(h)
            for i in range(length, len(path)):
                h = (h * base - path[i - length] * multiplier + path[i]) % MOD
                current_hashes.add(h)
            if common_hashes is None:
                common_hashes = current_hashes
            else:
                common_hashes &= current_hashes
                if not common_hashes:
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