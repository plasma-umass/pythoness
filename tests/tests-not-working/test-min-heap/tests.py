import minheap
import unittest


class TestMinHeap(unittest.TestCase):
    def setUp(self):
        self.h = minheap.MinHeap(elements=[2, 4, 5, 12, 13, 6, 10])

    def test_parent_index(self):
        self.assertLess(self.h._parent_index(0), 0)
        self.assertEqual(self.h._parent_index(1), 0)
        self.assertEqual(self.h._parent_index(2), 0)
        self.assertEqual(self.h._parent_index(4), 1)
        self.assertEqual(self.h._parent_index(6), 2)

    def test_left_child_index(self):
        self.assertGreaterEqual(self.h._left_child_index(3), len(self.h))
        self.assertGreaterEqual(self.h._left_child_index(5), len(self.h))
        self.assertEqual(self.h._left_child_index(0), 1)
        self.assertEqual(self.h._left_child_index(1), 3)
        self.assertEqual(self.h._left_child_index(2), 5)

    def test_right_child_index(self):
        self.assertGreaterEqual(self.h._right_child_index(3), len(self.h))
        self.assertGreaterEqual(self.h._right_child_index(6), len(self.h))
        self.assertEqual(self.h._right_child_index(0), 2)
        self.assertEqual(self.h._right_child_index(1), 4)
        self.assertEqual(self.h._right_child_index(2), 6)

    def test_is_empty(self):
        self.assertFalse(self.h.is_empty())
        self.assertTrue(minheap.MinHeap().is_empty())

    def test_peek(self):
        self.assertEqual(self.h.peek(), self.h.h[0])
        self.assertIsNone(minheap.MinHeap().peek())

    def test_heapify_init(self):
        elements = [2, 4, 5, 6, 10, 12, 13]
        h = minheap.MinHeap(elements)
        self.assertEqual(h.h, [2, 4, 5, 6, 10, 12, 13])

    def test_heapify_after_init(self):
        elements = [2, 4, 5, 6, 10, 12, 13]
        h = minheap.MinHeap()
        self.assertEqual(h.h, [])
        h._heapify(elements)
        self.assertEqual(h.h, [2, 4, 5, 6, 10, 12, 13])

    def test_insert_1(self):
        self.assertEqual(self.h.insert(1), 0)
        self.assertEqual(self.h.h, [1, 2, 5, 4, 13, 6, 10, 12])

    def test_insert_3(self):
        self.assertEqual(self.h.insert(3), 1)
        self.assertEqual(self.h.h, [2, 3, 5, 4, 13, 6, 10, 12])

    def test_insert_10(self):
        self.assertEqual(self.h.insert(9), 3)
        self.assertEqual(self.h.h, [2, 4, 5, 9, 13, 6, 10, 12])

    def test_insert_15(self):
        self.assertEqual(self.h.insert(15), 7)
        self.assertEqual(self.h.h, [2, 4, 5, 12, 13, 6, 10, 15])

    def test_update_min(self):
        self.assertTrue(9 not in self.h)
        self.assertTrue(10 in self.h)
        self.h.update_min(9, 10)
        self.assertTrue(9 in self.h)
        self.assertTrue(10 not in self.h)
        self.assertEqual(self.h.h, [2, 4, 5, 12, 13, 6, 9])

    def test_pop_empty(self):
        h = minheap.MinHeap()
        self.assertIsNone(h.pop())
        self.assertEqual(h.h, [])


class TestMinHeapWithTuples(unittest.TestCase):
    def setUp(self):
        self.h = minheap.MinHeap(
            elements=[(4, 101), (12, 9), (13, 5), (2, 1), (6, 1001), (5, 45), (10, 121)]
        )

    def test_correct_order(self):
        self.assertEqual(
            self.h.h,
            [(2, 1), (4, 101), (5, 45), (12, 9), (6, 1001), (13, 5), (10, 121)],
        )

    def test_insert_99_1(self):
        self.assertEqual(self.h.insert((1, 99)), 0)
        self.assertEqual(
            self.h.h,
            [
                (1, 99),
                (2, 1),
                (5, 45),
                (4, 101),
                (6, 1001),
                (13, 5),
                (10, 121),
                (12, 9),
            ],
        )

    def test_update_min(self):
        self.assertTrue((13, 5) in self.h)
        self.assertTrue((11, 5) not in self.h)
        self.h.update_min(11, 5)
        self.assertTrue((11, 5) in self.h)
        self.assertTrue((13, 5) not in self.h)
        self.assertEqual(
            self.h.h,
            [(2, 1), (4, 101), (5, 45), (12, 9), (6, 1001), (11, 5), (10, 121)],
        )

    def test_pop(self):
        self.assertEqual(len(self.h.h), 7)
        self.assertEqual(self.h.pop(), (2, 1))
        self.assertEqual(self.h.pop(), (4, 101))
        self.assertEqual(self.h.pop(), (5, 45))
        self.assertEqual(self.h.pop(), (6, 1001))
        self.assertEqual(len(self.h.h), 3)
        self.assertEqual(self.h.h, [(10, 121), (12, 9), (13, 5)])


if __name__ == '__main__':
    unittest.main()