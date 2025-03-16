# file: src/oracle3474.py:42-51
# asked: {"lines": [42, 46, 47, 48, 49, 50, 51], "branches": [[47, 48], [47, 51], [49, 47], [49, 50]]}
# gained: {"lines": [42, 46, 47, 48, 49, 50, 51], "branches": [[47, 48], [47, 51], [49, 47], [49, 50]]}

import pytest
from src.oracle3474 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_last_modifiable_position_all_modifiable(solution):
    modifiable = [True, True, True, True, True]
    result = solution._lastModifiablePosition(0, 5, modifiable)
    assert result == 4

def test_last_modifiable_position_none_modifiable(solution):
    modifiable = [False, False, False, False, False]
    result = solution._lastModifiablePosition(0, 5, modifiable)
    assert result == -1

def test_last_modifiable_position_some_modifiable(solution):
    modifiable = [False, True, False, True, False]
    result = solution._lastModifiablePosition(0, 5, modifiable)
    assert result == 3

def test_last_modifiable_position_partial_range(solution):
    modifiable = [False, True, False, True, False]
    result = solution._lastModifiablePosition(1, 3, modifiable)
    assert result == 3

def test_last_modifiable_position_out_of_bounds(solution):
    modifiable = [False, True, False, True, False]
    with pytest.raises(IndexError):
        solution._lastModifiablePosition(3, 3, modifiable)
