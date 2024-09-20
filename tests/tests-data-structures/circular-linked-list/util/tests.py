import unittest
from . import implementation as i


# class TestAppend(unittest.TestCase):
#     def test_append(self):
#         cll = i.CircularLinkedList()
#         cll.append(1)
#         cll.append(2)
#         cll.append(3)
#         self.assertEqual(cll.head.data, 1)
#         self.assertEqual(cll.head.next.data, 2)
#         self.assertEqual(cll.head.next.next.data, 3)
#         self.assertEqual(cll.head.next.next.next, cll.head)
# 
# class TestPrepend(unittest.TestCase):
#     def test_prepend(self):
#         cll = i.CircularLinkedList()
#         cll.prepend(1)
#         cll.prepend(2)
#         cll.prepend(3)
#         self.assertEqual(cll.head.data, 3)
#         self.assertEqual(cll.head.next.data, 2)
#         self.assertEqual(cll.head.next.next.data, 1)
#         self.assertEqual(cll.head.next.next.next, cll.head)
# 
# class TestDelete(unittest.TestCase):
#     def test_delete(self):
#         cll = i.CircularLinkedList()
#         cll.append(1)
#         cll.append(2)
#         cll.append(3)
#         cll.delete(2)
#         self.assertEqual(cll.head.data, 1)
#         self.assertEqual(cll.head.next.data, 3)
#         self.assertEqual(cll.head.next.next, cll.head)
#         
#         cll.delete(1)
#         self.assertEqual(cll.head.data, 3)
#         self.assertEqual(cll.head.next, cll.head)
#         
#         cll.delete(3)
#         self.assertIsNone(cll.head)
# 
#     def test_delete_single_node(self):
#         cll = i.CircularLinkedList()
#         cll.append(1)
#         cll.delete(1)
#         self.assertIsNone(cll.head)
# 
#     def test_delete_nonexistent(self):
#         cll = i.CircularLinkedList()
#         cll.append(1)
#         cll.append(2)
#         cll.delete(3)  # Deleting a nonexistent node should not alter the list
#         self.assertEqual(cll.head.data, 1)
#         self.assertEqual(cll.head.next.data, 2)
#         self.assertEqual(cll.head.next.next, cll.head)
# 
# 
# if __name__ == '__main__':
#     unittest.main()

import unittest
import io
from . import implementation as i

class TestCircularLinkedList(unittest.TestCase):
    def setUp(self):
        self.cll = i.CircularLinkedList()


    def test_append(self):
        self.cll.append(1)
        self.cll.append(2)
        self.cll.append(3)
        self.assertEqual(self.cll.head.data, 1)
        self.assertEqual(self.cll.head.next.data, 2)
        self.assertEqual(self.cll.head.next.next.data, 3)
        self.assertEqual(self.cll.head.next.next.next, self.cll.head)

    def test_prepend(self):
        self.cll.prepend(1)
        self.cll.prepend(2)
        self.cll.prepend(3)
        self.assertEqual(self.cll.head.data, 3)
        self.assertEqual(self.cll.head.next.data, 2)
        self.assertEqual(self.cll.head.next.next.data, 1)
        self.assertEqual(self.cll.head.next.next.next, self.cll.head)

    def test_delete(self):
        self.cll.append(1)
        self.cll.append(2)
        self.cll.append(3)
        self.cll.delete(2)
        self.assertEqual(self.cll.head.data, 1)
        self.assertEqual(self.cll.head.next.data, 3)
        self.assertEqual(self.cll.head.next.next, self.cll.head)
        
        self.cll.delete(1)
        self.assertEqual(self.cll.head.data, 3)
        self.assertEqual(self.cll.head.next, self.cll.head)
        
        self.cll.delete(3)
        self.assertIsNone(self.cll.head)

    def test_delete_single_node(self):
        self.cll.append(1)
        self.cll.delete(1)
        self.assertIsNone(self.cll.head)

    def test_delete_nonexistent(self):
        self.cll.append(1)
        self.cll.append(2)
        self.cll.delete(3)  # Deleting a nonexistent node should not alter the list
        self.assertNotEqual(self.cll.head.data, 1)
        self.assertEqual(self.cll.head.next.data, 2)
        self.assertEqual(self.cll.head.next.next, self.cll.head)



if __name__ == '__main__':
    unittest.main()
