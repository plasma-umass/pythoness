import pythoness
from typing import List

@pythoness.spec(
    """Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
You may not alter the values in the list's nodes, only nodes themselves may be changed.
 
Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000

 
Follow-up: Can you solve the problem in O(1) extra memory space?""",
    tests=[],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound="O(1)"
)
def reverseKGroup(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """"""

__init__()