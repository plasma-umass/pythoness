# file: src/oracle3229.py:4-21
# asked: {"lines": [4, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 19, 21], "branches": [[9, 12], [9, 21], [14, 15], [14, 16], [16, 17], [16, 19]]}
# gained: {"lines": [4, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 19, 21], "branches": [[9, 12], [9, 21], [14, 15], [14, 16], [16, 17], [16, 19]]}

import pytest
from src.oracle3229 import Solution
import itertools

@pytest.fixture
def solution():
    return Solution()

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def test_minimum_operations_case1(solution, monkeypatch):
    nums = [1, 2, 3]
    target = [1, 2, 3]
    monkeypatch.setattr(itertools, 'pairwise', pairwise)
    assert solution.minimumOperations(nums, target) == 0

def test_minimum_operations_case2(solution, monkeypatch):
    nums = [1, 3, 2]
    target = [2, 1, 3]
    monkeypatch.setattr(itertools, 'pairwise', pairwise)
    assert solution.minimumOperations(nums, target) == 4

def test_minimum_operations_case3(solution, monkeypatch):
    nums = [3, 1, 2]
    target = [1, 3, 2]
    monkeypatch.setattr(itertools, 'pairwise', pairwise)
    assert solution.minimumOperations(nums, target) == 4

def test_minimum_operations_case4(solution, monkeypatch):
    nums = [1, 2, 3]
    target = [3, 2, 1]
    monkeypatch.setattr(itertools, 'pairwise', pairwise)
    assert solution.minimumOperations(nums, target) == 4

def test_minimum_operations_case5(solution, monkeypatch):
    nums = [1, 2, 3]
    target = [2, 3, 4]
    monkeypatch.setattr(itertools, 'pairwise', pairwise)
    assert solution.minimumOperations(nums, target) == 1
