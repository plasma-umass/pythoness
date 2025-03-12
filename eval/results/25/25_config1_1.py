import pythoness
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


@pythoness.spec(
    """Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
You may not alter the values in the list's nodes, only nodes themselves may be changed.

Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000""",
    tests=[
        "reverseKGroup(head = [1,2,3,4,5], k = 2) == [2,1,4,3,5]",
        "reverseKGroup(head = [1,2,3,4,5], k = 3) == [3,2,1,4,5]",
    ],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def reverseKGroup(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """"""


reverseKGroup(head=[1, 2, 3, 4, 5], k=2)
