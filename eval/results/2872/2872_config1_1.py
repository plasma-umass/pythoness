import pythoness
from typing import List, Optional

def maxKDivisibleComponents(n: int, edges: List[List[int]], values: List[int], k: int) -> int:
    """
    There is an undirected tree with n nodes labeled from 0 to n - 1. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
    You are also given a 0-indexed integer array values of length n, where values[i] is the value associated with the i^th node, and an integer k.
    A valid split of the tree is obtained by removing any set of edges, possibly empty, from the tree such that the resulting components all have values that are divisible by k, where the value of a connected component is the sum of the values of its nodes.
    Return the maximum number of components in any valid split.
    """
    from collections import defaultdict

    def dfs(node, parent):
        subtree_sum = values[node]
        for neighbor in tree[node]:
            if neighbor != parent:
                subtree_sum += dfs(neighbor, node)
        # If the subtree sum including this node is divisible by k, we can consider it as a component and exclude the edge from parent.
        if subtree_sum % k == 0:
            nonlocal max_components
            max_components += 1
            return 0  # If the component is valid, return 0 since we don't carry over any value upwards.
        return subtree_sum  # If not valid, return the subtree_sum to parent.
    # Create adjacency list for the undirected tree.
    tree = defaultdict(list)
    for (a, b) in edges:
        tree[a].append(b)
        tree[b].append(a)
    # We start with 0 components because we need at least one whole tree component to start with.
    max_components = 0
    root_to_all_sum = dfs(0, -1)  # Start dfs from any node, here node 0
    return max_components
maxKDivisibleComponents(n=5, edges=[[0, 2], [1, 2], [1, 3], [2, 4]], values=[1, 8, 1, 4, 4], k=6)