# file: src/oracle3454.py:4-34
# asked: {"lines": [4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 27, 29, 30, 33, 34], "branches": [[14, 15], [14, 16], [16, 17], [16, 19], [23, 24], [23, 26], [26, 27], [26, 29]]}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 27, 29, 30, 33, 34], "branches": [[14, 15], [14, 16], [16, 17], [16, 19], [23, 24], [23, 26], [26, 27], [26, 29]]}

import pytest
from src.oracle3454 import SegmentTree

@pytest.fixture
def segment_tree():
    return SegmentTree([0, 1, 2, 3, 4, 5])

def test_update_no_overlap(segment_tree):
    segment_tree.update(5, 6, 1, 0, segment_tree.n - 1, 0)
    assert segment_tree.covered == [0] * (4 * segment_tree.n)

def test_update_full_overlap(segment_tree):
    segment_tree.update(0, 5, 1, 0, segment_tree.n - 1, 0)
    assert segment_tree.covered[0] == 5

def test_update_partial_overlap(segment_tree):
    segment_tree.update(1, 3, 1, 0, segment_tree.n - 1, 0)
    assert segment_tree.covered[0] == 2

def test_update_partial_overlap_with_removal(segment_tree):
    segment_tree.update(1, 3, 1, 0, segment_tree.n - 1, 0)
    segment_tree.update(1, 3, -1, 0, segment_tree.n - 1, 0)
    assert segment_tree.covered[0] == 0

def test_query(segment_tree):
    segment_tree.update(0, 5, 1, 0, segment_tree.n - 1, 0)
    assert segment_tree.query() == 5
