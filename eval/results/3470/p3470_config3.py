import pythoness
from typing import List, Optional

@pythoness.spec(
    """Returns the k-th lexicographically sorted alternating permutation of the first n positive integers.
An alternating permutation ensures no two adjacent elements are both odd or both even.
If fewer than k valid permutations exist, returns an empty list.""",
    tests=["""permute(n=5, k=10) == [5, 2, 3, 4, 1]""", """permute(n=7, k=20) == [1, 4, 5, 6, 7, 2, 3]""", """permute(n=4, k=5) == [3, 2, 1, 4]""", """permute(n=8, k=30) == [1, 2, 7, 6, 3, 8, 5, 4]""", """permute(n=12, k=500) == [1, 2, 3, 4, 11, 8, 9, 10, 7, 12, 5, 6]""", """permute(n=20, k=2000) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 15, 20, 17, 14, 19, 16, 13, 12]""", """permute(n=25, k=50000) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 21, 20, 17, 24, 15, 22, 23, 18, 25, 16, 19]""", """permute(n=50, k=1000000) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 40, 49, 46, 43, 42, 39, 44, 47, 38, 45, 50, 41, 48]""", """permute(n=40, k=100000) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 30, 39, 38, 35, 34, 37, 32, 33, 40, 29, 36]""", """permute(n=60, k=10000000) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 51, 58, 49, 56, 55, 50, 47, 52, 59, 48, 57, 60, 53, 54]"""],
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def permute(n: int, k: int) -> List[int]:
    """"""

permute(n=5, k=10) 