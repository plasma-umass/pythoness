import pythoness
from typing import List, Optional

def maxKDivisibleComponents(n: int, edges: List[List[int]], values: List[int], k: int) -> int:
    """
    There is an undirected tree with n nodes labeled from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, 
    where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
    You are also given a 0-indexed integer array values of length n, where values[i] is the value associated with the ith node, and an integer k.
    A valid split of the tree is obtained by removing any set of edges, possibly empty, from the tree such that the resulting components all have 
    values that are divisible by k, where the value of a connected component is the sum of the values of its nodes.
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
    # Create adjacency list for the tree
    tree = defaultdict(list)
    for (u, v) in edges:
        tree[u].append(v)
        tree[v].append(u)
    # This will hold the count of maximum k-divisible components
    max_components = 0
    # Function to recursively perform DFS from a node

    def dfs(node, parent):
        nonlocal max_components
        current_sum = values[node]
        for neighbour in tree[node]:
            if neighbour != parent:
                child_sum = dfs(neighbour, node)
                current_sum += child_sum
        if current_sum % k == 0:
            max_components += 1
            return 0
        return current_sum
    # Start DFS from node 0 (or any arbitrary node, since it's a connected tree)
    dfs(0, -1)
    return max_components
maxKDivisibleComponents(n=5, edges=[[0, 2], [1, 2], [1, 3], [2, 4]], values=[1, 8, 1, 4, 4], k=6)