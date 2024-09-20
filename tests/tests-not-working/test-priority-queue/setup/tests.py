import unittest

from . import priority_queue as prq


class AddTest(unittest.TestCase):
        
    def test_add(self):    
        p = prq.PriorityQueue()
        p.add(1, 10)


class PeekTest(unittest.TestCase):

    def test_peek(self):
        p = prq.PriorityQueue()
        self.assertEqual(p.peek(), None)
        p.add(1,4)
        self.assertEqual(p.peek(), 1)

class PopTest (unittest.TestCase):
    
    def test_pop(self):
        p = prq.PriorityQueue()
        p.add(1, 10)
        p.add(2, 9)
        p.add(3, 8)
        p.add(4, 7)
        self.assertEqual(p.pop(), 1)
        self.assertEqual(p.pop(), 2)
        self.assertEqual(p.pop(), 3)
        self.assertEqual(p.pop(), 4)