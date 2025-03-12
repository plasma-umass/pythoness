import pythoness
from typing import List, Optional

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
    # Build the tree as an adjacency list
    tree = defaultdict(list)
    for (a, b) in edges:
        tree[a].append(b)
        tree[b].append(a)
    # Helper function to perform DFS and calculate component sums

    def dfs(node, parent):
        total = values[node]
        for neighbor in tree[node]:
            if neighbor == parent:
                continue
            total += dfs(neighbor, node)
        # We can form a valid component if the subtree sum is divisible by k
        if total % k == 0:
            nonlocal components
            components += 1
            return 0
        else:
            return total
    components = 0
    # Start DFS from any node, considering 0 here as root
    dfs(0, -1)
    return components
maxKDivisibleComponents(n=5, edges=[[0, 2], [1, 2], [1, 3], [2, 4]], values=[1, 8, 1, 4, 4], k=6)