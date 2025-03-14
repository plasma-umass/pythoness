# file: src/oracle699.py:4-12
# asked: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12], "branches": []}
# gained: {"lines": [4, 5, 6, 7, 8, 9, 10, 11, 12], "branches": []}

import pytest
from src.oracle699 import Node

def test_node_initialization():
    # Test initialization of Node
    l, r = 0, 10
    node = Node(l, r)
    
    assert node.left is None
    assert node.right is None
    assert node.l == l
    assert node.r == r
    assert node.mid == (l + r) >> 1
    assert node.v == 0
    assert node.add == 0
