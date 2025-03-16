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

    def rolling_hash(path, length, base, mod):
        curr_hash = 0
        base_powers = [1] * (len(path) + 1)
        for i in range(1, len(base_powers)):
            base_powers[i] = base_powers[i - 1] * base % mod
        for i in range(length):
            curr_hash = (curr_hash * base + path[i]) % mod
        hashes = defaultdict(list)
        hashes[curr_hash].append(0)
        for i in range(length, len(path)):
            curr_hash = (curr_hash * base - path[i - length] * base_powers[length] + path[i]) % mod
            if curr_hash < 0:
                curr_hash += mod
            hashes[curr_hash].append(i - length + 1)
        return hashes

    def valid(length):
        base = 257
        mod1 = 10 ** 9 + 7
        mod2 = 10 ** 9 + 9
        all_plain_hashes1 = rolling_hash(paths[0], length, base, mod1)
        all_plain_hashes2 = rolling_hash(paths[0], length, base, mod2)
        for i in range(1, len(paths)):
            path_hashes1 = rolling_hash(paths[i], length, base, mod1)
            path_hashes2 = rolling_hash(paths[i], length, base, mod2)
            new_all_plain_hashes1 = defaultdict(list)
            new_all_plain_hashes2 = defaultdict(list)
            for h1 in path_hashes1:
                if h1 in all_plain_hashes1:
                    new_all_plain_hashes1[h1] = min(all_plain_hashes1[h1], path_hashes1[h1])
            all_plain_hashes1 = new_all_plain_hashes1
            for h2 in path_hashes2:
                if h2 in all_plain_hashes2:
                    new_all_plain_hashes2[h2] = min(all_plain_hashes2[h2], path_hashes2[h2])
            all_plain_hashes2 = new_all_plain_hashes2
            if not all_plain_hashes1 or not all_plain_hashes2:
                return False
        return True
    (left, right) = (0, min((len(path) for path in paths)))
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        if valid(mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    return answer
longestCommonSubpath(n=5, paths=[[0, 1, 2, 3, 4], [2, 3, 4], [4, 0, 1, 2, 3]])