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
    from typing import List

    def check_length(L: int) -> bool:
        """ Check if there exists a common subpath of length L """
        (R, P) = (10 ** 9 + 7, 10 ** 9 + 9)
        base = 1
        for _ in range(L):
            base = base * P % R

        def compute_hashes(path):
            current_hash = 0
            hashes = set()
            for i in range(len(path)):
                current_hash = (current_hash * P + path[i]) % R
                if i >= L:
                    current_hash = (current_hash - path[i - L] * base) % R
                if i >= L - 1:
                    hashes.add(current_hash)
            return hashes
        hashes = compute_hashes(paths[0])
        for path in paths[1:]:
            hashes &= compute_hashes(path)
            if not hashes:
                return False
        return len(hashes) > 0
    (left, right) = (0, min((len(p) for p in paths)) + 1)
    while left < right:
        mid = (left + right) // 2
        if check_length(mid):
            left = mid + 1
        else:
            right = mid
    return left - 1
longestCommonSubpath(n=5, paths=[[0, 1, 2, 3, 4], [2, 3, 4], [4, 0, 1, 2, 3]])