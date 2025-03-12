import pythoness
from typing import List, Optional

class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    """
    You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
    Merge all the linked-lists into one sorted linked-list and return it.

    Definition for singly-linked list.
    class ListNode:
    def __init__(self, val=0, next=None):
    self.val = val
    self.next = next

    Constraints:

    k == lists.length
    0 <= k <= 10^4
    0 <= lists[i].length <= 500
    -10^4 <= lists[i][j] <= 10^4
    lists[i] is sorted in ascending order.
    The sum of lists[i].length will not exceed 10^4.
    """
    import heapq

    class Wrapper:

        def __init__(self, node):
            self.node = node

        def __lt__(self, other):
            return self.node.val < other.node.val
    min_heap = []
    for l in lists:
        current = ListNode(0)
        dummy = current
        for value in l:
            current.next = ListNode(value)
            current = current.next
        if dummy.next:
            heapq.heappush(min_heap, Wrapper(dummy.next))
    head = point = ListNode(0)
    while min_heap:
        node = heapq.heappop(min_heap).node
        point.next = node
        point = point.next
        if node.next:
            heapq.heappush(min_heap, Wrapper(node.next))
    # Convert the linked list back to a list for comparison
    result = []
    current = head.next
    while current:
        result.append(current.val)
        current = current.next
    return result
mergeKLists(lists=[[1, 4, 5], [1, 3, 4], [2, 6]])