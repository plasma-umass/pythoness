# file: src/oracle1416.py:4-34
# asked: {"lines": [4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 27, 29, 30, 33, 34], "branches": [[14, 15], [14, 16], [16, 17], [16, 19], [23, 24], [23, 26], [26, 27], [26, 29]]}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 26, 29, 30, 33, 34], "branches": [[14, 15], [14, 16], [16, 17], [16, 19], [23, 24], [23, 26], [26, 29]]}

import pytest
from src.oracle1416 import SegmentTree

def test_segment_tree_update_no_overlap():
    xs = [1, 2, 3, 4, 5]
    tree = SegmentTree(xs)
    tree.update(6, 7, 1, 0, len(xs) - 2, 0)
    assert tree.covered[0] == 0

def test_segment_tree_update_full_overlap():
    xs = [1, 2, 3, 4, 5]
    tree = SegmentTree(xs)
    tree.update(1, 5, 1, 0, len(xs) - 2, 0)
    assert tree.covered[0] == 4

def test_segment_tree_update_partial_overlap():
    xs = [1, 2, 3, 4, 5]
    tree = SegmentTree(xs)
    tree.update(2, 4, 1, 0, len(xs) - 2, 0)
    assert tree.covered[0] == 2

def test_segment_tree_query():
    xs = [1, 2, 3, 4, 5]
    tree = SegmentTree(xs)
    tree.update(1, 5, 1, 0, len(xs) - 2, 0)
    assert tree.query() == 4

@pytest.fixture(autouse=True)
def run_around_tests(monkeypatch):
    # Setup: before each test
    yield
    # Teardown: after each test
    monkeypatch.undo()
