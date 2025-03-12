import pythoness
from typing import List, Optional

@pythoness.spec(
    """You are given an integer array nums of length n and an integer array queries.
Let gcdPairs denote an array obtained by calculating the GCD of all possible pairs (nums[i], nums[j]), where 0 <= i < j < n, and then sorting these values in ascending order.
For each query queries[i], you need to find the element at index queries[i] in gcdPairs.
Return an integer array answer, where answer[i] is the value at gcdPairs[queries[i]] for each query.
The term gcd(a, b) denotes the greatest common divisor of a and b.
 
Constraints:

2 <= n == nums.length <= 10^5
1 <= nums[i] <= 5 * 10^4
1 <= queries.length <= 10^5
0 <= queries[i] < n * (n - 1) / 2""",
    tests=['gcdValues(nums = [2,3,4], queries = [0,2,2]) == [1,2,2]', 'gcdValues(nums = [4,4,2,1], queries = [5,3,1,0]) == [4,2,1,1]', 'gcdValues(nums = [2,2], queries = [0,0]) == [2,2]'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def gcdValues(nums: List[int], queries: List[int]) -> List[int]:
    """"""

gcdValues(nums = [2,3,4], queries = [0,2,2]) 