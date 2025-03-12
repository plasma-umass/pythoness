import pythoness
from typing import List, Optional


@pythoness.spec(
    """You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
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
The sum of lists[i].length will not exceed 10^4.""",
    tests=[
        "mergeKLists(lists = [[1,4,5],[1,3,4],[2,6]]) == [1,1,2,3,4,4,5,6]",
        "mergeKLists(lists = []) == []",
        "mergeKLists(lists = [[]]) == []",
    ],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    replace=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """"""


mergeKLists(lists=[[1, 4, 5], [1, 3, 4], [2, 6]])
