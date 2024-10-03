from . import implementation as i
import unittest


class TestInsertInOrder(unittest.TestCase):
    def test_insert_and_inorder(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(20)
        bst.insert(40)
        bst.insert(70)
        bst.insert(60)
        bst.insert(80)
        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 70, 80])


class TestSearch(unittest.TestCase):

    def test_search(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        self.assertIsNotNone(bst.search(30))
        self.assertIsNone(bst.search(100))


class TestDelete(unittest.TestCase):
    def test_delete_node_with_no_children(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.delete(70)
        self.assertEqual(bst.inorder(), [30, 50])

    def test_delete_node_with_one_child(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.delete(30)
        self.assertEqual(bst.inorder(), [20, 50, 70])

    def test_delete_node_with_two_children(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        bst.delete(30)
        self.assertEqual(bst.inorder(), [20, 40, 50, 70])


class TestPreorder(unittest.TestCase):

    def test_preorder_traversal(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        self.assertEqual(bst.preorder(), [50, 30, 20, 40, 70])


class TestPostorder(unittest.TestCase):

    def test_postorder_traversal(self):
        bst = i.BinarySearchTree()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(20)
        bst.insert(40)
        self.assertEqual(bst.postorder(), [20, 40, 30, 70, 50])
