import pythoness
from . import tests

class PriorityQueue(object):
    """Implementation of a Priority Queue, largest priority goes first"""

    @pythoness.spec("""Sets the necessary parts of a priority queue""")
    def __init__(self):
        ""

    @pythoness.spec("Adds a new node, which is a tuple of (value, priority)", related_objs=['cls'])
    def add(self, value, priority):
        ""

    @pythoness.spec("Returns the element of largest priority without removing it from the queue",
                    tests = [tests.PeekTest], related_objs=['cls'])
    def peek(self):
        ""

    @pythoness.spec("Removes and returns the element in the queue of largest priority",
                    tests = [tests.PopTest], related_objs=['cls'])
    def pop(self):
        ""








