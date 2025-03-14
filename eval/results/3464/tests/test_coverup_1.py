# file: src/oracle3464.py:4-17
# asked: {"lines": [4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17], "branches": []}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17], "branches": []}

import pytest
from src.oracle3464 import Sequence

def test_sequence_iteration():
    seq = Sequence(startX=1, startY=2, endX=3, endY=4, length=5)
    iter_seq = iter(seq)
    assert next(iter_seq) == 1
    assert next(iter_seq) == 2
    assert next(iter_seq) == 3
    assert next(iter_seq) == 4
    assert next(iter_seq) == 5

    with pytest.raises(StopIteration):
        next(iter_seq)
