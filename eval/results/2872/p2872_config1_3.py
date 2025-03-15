import pythoness
from typing import List, Optional
from typing import List

def maxKDivisibleComponents(n: int, edges: List[List[int]], values: List[int], k: int) -> int:
    """
    There is an undirected tree with n nodes labeled from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
    You are also given a 0-indexed integer array values of length n, where values[i] is the value associated with the i^th node, and an integer k.
    A valid split of the tree is obtained by removing any set of edges, possibly empty, from the tree such that the resulting components all have values that are divisible by k, where the value of a connected component is the sum of the values of its nodes.
    Return the maximum number of components in any valid split.

    Constraints:

    1 <= n <= 3 * 10^4
    edges.length == n - 1
    edges[i].length == 2
    0 <= ai, bi < n
    values.length == n
    0 <= values[i] <= 10^9
    1 <= k <= 10^9
    Sum of values is divisible by k.
    The input is generated such that edges represents a valid tree.
    """
    from collections import defaultdict
    # Build adjacency list
    adj_list = defaultdict(list)
    for (u, v) in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    def dfs(node, parent):
        component_sum = values[node]
        for neighbor in adj_list[node]:
            if neighbor == parent:
                continue
            component_sum += dfs(neighbor, node)
        # If component_sum is divisible by k, we can make it a new component
        if component_sum % k == 0:
            nonlocal max_components
            max_components += 1
            return 0  # Return 0 to 'cut off' this component and not carry its sum upward
        return component_sum  # Otherwise return its sum upward to its parent
    max_components = 0
    # Start DFS from an arbitrary root node (e.g., node 0)
    dfs(0, -1)
    return max_components
maxKDivisibleComponents(n=5, edges=[[0, 2], [1, 2], [1, 3], [2, 4]], values=[1, 8, 1, 4, 4], k=6)