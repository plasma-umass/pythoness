import pythoness
from typing import List, Optional

def gcdValues(nums: List[int], queries: List[int]) -> List[int]:
    """
    You are given an integer array nums of length n and an integer array queries.
    Let gcdPairs denote an array obtained by calculating the GCD of all possible pairs (nums[i], nums[j]),
    where 0 <= i < j < n, and then sorting these values in ascending order.
    For each query queries[i], you need to find the element at index queries[i] in gcdPairs.
    Return an integer array answer, where answer[i] is the value at gcdPairs[queries[i]] for each query.
    The term gcd(a, b) denotes the greatest common divisor of a and b.

    Constraints:

    2 <= n == nums.length <= 10^5
    1 <= nums[i] <= 5 * 10^4
    1 <= queries.length <= 10^5
    0 <= queries[i] < n * (n - 1) / 2
    """
    from math import gcd
    from itertools import combinations
    gcdPairs = []
    n = len(nums)
    for (i, j) in combinations(range(n), 2):
        gcdPairs.append(gcd(nums[i], nums[j]))
    gcdPairs.sort()
    answer = [gcdPairs[query] for query in queries]
    return answer
gcdValues(nums=[2, 3, 4], queries=[0, 2, 2])