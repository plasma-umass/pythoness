import pythoness
from . import tests


class Node:
    "A Node for BinarySearchTree"

    __slots__ = ["left", "right", "value"]

    def __init__(self, key):
        "Initializes a node of left and right children with value key"
        self.left = None
        self.right = None
        self.value = key


class BinarySearchTree:
    "A binary search tree"

    __slots__ = ["head"]

    @pythoness.spec("Initializes the head of the BST", related_objs=[Node])
    def __init__(self):
        """"""

    @pythoness.spec(
        "Inserts a node with value key into the BST",
        related_objs=[Node, __init__],
        tests=[tests.TestInsertInOrder],
    )
    def _insert(self, node, key):
        """"""

    @pythoness.spec(
        "Inserts a node with value key into the BST",
        related_objs=[_insert],
        tests=[tests.TestInsertInOrder],
    )
    def insert(self, key):
        """"""

    @pythoness.spec(
        "searches the tree for a node with value key",
        related_objs=[Node, __init__],
        tests=[tests.TestSearch],
    )
    def _search(self, node, key):
        """"""

    @pythoness.spec(
        "searches the tree for a node with value key",
        related_objs=[_search],
        tests=[tests.TestSearch],
    )
    def search(self, key):
        """"""

    @pythoness.spec(
        "Gets the minimum value node in the BST", related_objs=[Node, __init__]
    )
    def _min_value_node(self, node):
        """"""

    @pythoness.spec(
        "Deletes a node in the tree with value key",
        related_objs=[Node, __init__, search, _min_value_node],
        tests=[tests.TestDelete],
    )
    def _delete(self, node, key):
        """"""

    @pythoness.spec(
        "Deletes a node in the tree with value key",
        related_objs=[_delete],
        tests=[tests.TestDelete],
    )
    def delete(self, key):
        """"""

    @pythoness.spec(
        "returns the inorder traversal of the BST",
        related_objs=[Node, __init__],
        tests=[tests.TestInsertInOrder],
    )
    def _inorder(self, node):
        """"""

    @pythoness.spec(
        "returns the inorder traversal of the BST",
        related_objs=[_inorder],
        tests=[tests.TestInsertInOrder],
    )
    def inorder(self):
        """"""

    @pythoness.spec(
        "returns the preorder traversal of the BST",
        related_objs=[Node, __init__],
        tests=[tests.TestPreorder],
    )
    def _preorder(self, node):
        """"""

    @pythoness.spec(
        "returns the preorder traversal of the BST",
        related_objs=[Node, _preorder],
        tests=[tests.TestPreorder],
    )
    def preorder(self):
        """"""

    @pythoness.spec(
        "returns the postorder traversal of the BST",
        related_objs=[Node, __init__],
        tests=[tests.TestPostorder],
    )
    def _postorder(self, node):
        """"""

    @pythoness.spec(
        "returns the postorder traversal of the BST",
        related_objs=[_postorder],
        tests=[tests.TestPostorder],
    )
    def postorder(self):
        """"""
