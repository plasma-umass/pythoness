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
    # Build the tree adjacency list
    tree = defaultdict(list)
    for (a, b) in edges:
        tree[a].append(b)
        tree[b].append(a)
    visited = [False] * n
    non_divisible_edges = 0

    def dfs(node):
        nonlocal non_divisible_edges
        visited[node] = True
        current_sum = values[node]
        for neighbor in tree[node]:
            if not visited[neighbor]:
                child_sum = dfs(neighbor)
                if child_sum % k != 0:
                    non_divisible_edges += 1
                current_sum += child_sum
        return current_sum
    # Start DFS traversal from node 0
    dfs(0)
    # The maximum number of components is the original node count
    # minus edges we can't remove (those that don't result in a valid division)
    return n - non_divisible_edges
maxKDivisibleComponents(n=5, edges=[[0, 2], [1, 2], [1, 3], [2, 4]], values=[1, 8, 1, 4, 4], k=6)