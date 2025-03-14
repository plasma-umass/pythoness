# file: src/oracle25.py:1-4
# asked: {"lines": [1, 2, 3, 4], "branches": []}
# gained: {"lines": [1, 2, 3, 4], "branches": []}

import pytest
from src.oracle25 import ListNode

def test_list_node_initialization():
    # Test default initialization
    node = ListNode()
    assert node.val == 0
    assert node.next is None

    # Test initialization with custom value
    node = ListNode(val=5)
    assert node.val == 5
    assert node.next is None

    # Test initialization with custom value and next node
    next_node = ListNode(val=10)
    node = ListNode(val=5, next=next_node)
    assert node.val == 5
    assert node.next == next_node
    assert node.next.val == 10

