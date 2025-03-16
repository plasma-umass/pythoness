# file: src/oracle23.py:10-27
# asked: {"lines": [10, 11, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 24, 25, 27], "branches": [[16, 17], [16, 20], [17, 16], [17, 18], [20, 21], [20, 27], [22, 23], [22, 24]]}
# gained: {"lines": [10, 11, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 24, 25, 27], "branches": [[16, 17], [16, 20], [17, 16], [17, 18], [20, 21], [20, 27], [22, 23], [22, 24]]}

import pytest
from src.oracle23 import Solution, ListNode

def list_to_nodes(lst):
    """Helper function to convert a list to ListNode."""
    dummy = ListNode(0)
    current = dummy
    for value in lst:
        current.next = ListNode(value)
        current = current.next
    return dummy.next

def nodes_to_list(node):
    """Helper function to convert ListNode to a list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

def test_mergeKLists_empty():
    solution = Solution()
    result = solution.mergeKLists([])
    assert result is None

def test_mergeKLists_single_empty_list():
    solution = Solution()
    result = solution.mergeKLists([None])
    assert result is None

def test_mergeKLists_single_list():
    solution = Solution()
    list1 = list_to_nodes([1, 2, 3])
    result = solution.mergeKLists([list1])
    assert nodes_to_list(result) == [1, 2, 3]

def test_mergeKLists_multiple_lists():
    solution = Solution()
    list1 = list_to_nodes([1, 4, 5])
    list2 = list_to_nodes([1, 3, 4])
    list3 = list_to_nodes([2, 6])
    result = solution.mergeKLists([list1, list2, list3])
    assert nodes_to_list(result) == [1, 1, 2, 3, 4, 4, 5, 6]

def test_mergeKLists_lists_with_none():
    solution = Solution()
    list1 = list_to_nodes([1, 4, 5])
    list2 = None
    list3 = list_to_nodes([2, 6])
    result = solution.mergeKLists([list1, list2, list3])
    assert nodes_to_list(result) == [1, 2, 4, 5, 6]
