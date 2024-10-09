import pythoness
from . import tests


class Node:
    "A Node for CircularLinkedList"

    @pythoness.spec("Initializes the node")
    def __init__(self, data):
        """"""


class CircularLinkedList:
    "A Circular Linked List"

    @pythoness.spec("Initializes the list", related_objs=[Node])
    def __init__(self):
        """"""

    @pythoness.spec(
        "Adds a node with given data to the end of the list",
        tests=[tests.TestCircularLinkedList],
        related_objs=[__init__, Node],
    )
    def append(self, data):
        """"""

    @pythoness.spec(
        "Adds a node with given data to the beginning of the list",
        tests=[tests.TestCircularLinkedList],
        related_objs=[__init__, Node],
    )
    def prepend(self, data):
        """"""

    @pythoness.spec(
        "Deletes the node in the list with data key",
        tests=[tests.TestCircularLinkedList],
        related_objs=[__init__, Node],
    )
    def delete(self, key):
        """"""

    @pythoness.spec(
        "Prints the circular linked list in the form: [element1 element2 element3...]",
        related_objs=[__init__, Node],
    )
    def print_list(self):
        """"""
