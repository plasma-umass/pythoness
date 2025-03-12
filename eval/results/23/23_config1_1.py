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
    from typing import List, Optional

    class ListNode:

        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
    ListNode.__lt__ = lambda self, other: self.val < other.val

    def array_to_linked_list(arr):
        """Helper function to convert array to linked list"""
        head = ListNode() if arr else None
        current = head
        for num in arr:
            current.next = ListNode(num)
            current = current.next
        return head.next if head else None

    def linked_list_to_array(node):
        """Helper function to convert linked list to array"""
        arr = []
        while node:
            arr.append(node.val)
            node = node.next
        return arr
    # Convert input arrays to linked lists
    linked_lists = [array_to_linked_list(l) for l in lists]
    min_heap = []
    for node in linked_lists:
        if node:
            heapq.heappush(min_heap, node)
    dummy = ListNode()
    current = dummy
    while min_heap:
        node = heapq.heappop(min_heap)
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(min_heap, node.next)
    merged_array = linked_list_to_array(dummy.next)
    return merged_array
mergeKLists(lists=[[1, 4, 5], [1, 3, 4], [2, 6]])