from . import implementation as i
import unittest


class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        self.bst = i.BinarySearchTree()

    def test_insert_and_inorder(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(20)
        self.bst.insert(40)
        self.bst.insert(70)
        self.bst.insert(60)
        self.bst.insert(80)
        self.assertEqual(self.bst.inorder(), [20, 30, 40, 50, 60, 70, 80])

    def test_search(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.assertIsNotNone(self.bst.search(30))
        self.assertIsNone(self.bst.search(100))

    def test_delete_node_with_no_children(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.bst.delete(70)
        self.assertEqual(self.bst.inorder(), [30, 50])

    def test_delete_node_with_one_child(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.bst.insert(20)
        self.bst.delete(30)
        self.assertEqual(self.bst.inorder(), [20, 50, 70])

    def test_delete_node_with_two_children(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.bst.insert(20)
        self.bst.insert(40)
        self.bst.delete(30)
        self.assertEqual(self.bst.inorder(), [20, 40, 50, 70])

    def test_preorder_traversal(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.bst.insert(20)
        self.bst.insert(40)
        self.assertEqual(self.bst.preorder(), [50, 30, 20, 40, 70])

    def test_postorder_traversal(self):
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.bst.insert(20)
        self.bst.insert(40)
        self.assertEqual(self.bst.postorder(), [20, 40, 30, 70, 50])
