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

    def rolling_hash(base: int, mod: int, length: int, path: List[int]):
        current_hash = 0
        base_l = 1
        for i in range(length):
            current_hash = (current_hash * base + path[i]) % mod
            base_l = base_l * base % mod
        yield (current_hash, base_l)
        for i in range(length, len(path)):
            current_hash = (current_hash * base - path[i - length] * base_l + path[i]) % mod
            yield (current_hash, base_l)

    def check(length: int) -> bool:
        seen_hashes = set()
        base = 10 ** 4 + 7
        mod = 2 ** 63 - 1
        for (i, path) in enumerate(paths):
            current_hashes = set((hash_val for (hash_val, _) in rolling_hash(base, mod, length, path)))
            if i == 0:
                seen_hashes = current_hashes
            else:
                seen_hashes &= current_hashes
            if not seen_hashes:
                return False
        return True
    (left, right) = (0, min((len(path) for path in paths)))
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        if check(mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    return answer
longestCommonSubpath(n=5, paths=[[0, 1, 2, 3, 4], [2, 3, 4], [4, 0, 1, 2, 3]])