import pythoness
from typing import List

@pythoness.spec(
    """A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.
The path sum of a path is the sum of the node's values in the path.
Given the root of a binary tree, return the maximum path sum of any non-empty path.
 
Constraints:

The number of nodes in the tree is in the range [1, 3 * 10^4].
-1000 <= Node.val <= 1000""",
    tests=['__init__(root = [1,2,3]) == 6', '__init__(root = [-10,9,20,null,null,15,7]) == 42'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def maxPathSum(root: Optional[TreeNode]) -> int:
    """"""

__init__()