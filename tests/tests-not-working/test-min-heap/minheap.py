import pythoness
import tests


class MinHeap:
    """MinHeap implementation.

    Supported operations:
        is_empty():                 Check whether the heap is empty or not.
        peek():                     Return the current smallest heap element.
        insert(element):            Insert element into heap and re-heapify heap.
        pop():                      Return smallest heap element and re-heapify heap.
        update_min(value, label):   Update comparison value of an element in heap.

    Usage:
        >>> h = MinHeap([10, 5, 2, 8, -1, 9])
        >>> h.insert(3)
        2
        >>> h
        [-1, 2, 3, 10, 8, 9, 5]
        >>> ordered = []
        >>> while not h.is_empty():
        ...     ordered.append(h.pop())
        >>> ordered
        [-1, 2, 3, 5, 8, 9, 10]

        >>> h = MinHeap([(10, 'J'), (5, 'E'), (2, 'B'), (8, 'H'), (9, 'I')])
        >>> h.insert((1, 'A'))
        0
        >>> h
        [(1, 'A'), (8, 'H'), (2, 'B'), (10, 'J'), (9, 'I'), (5, 'E')]
        >>> h.update_min(7, 'I')
        (7, 'I')
        >>> h
        [(1, 'A'), (7, 'I'), (2, 'B'), (10, 'J'), (8, 'H'), (5, 'E')]
        >>> ordered = []
        >>> while not h.is_empty():
        ...     ordered.append(h.pop())
        >>> ordered
        [(1, 'A'), (2, 'B'), (5, 'E'), (7, 'I'), (8, 'H'), (10, 'J')]

    Note:
        Elements can be tuples (value, label) which can be useful for tracking
        comparison values of records such as node names i.e. (3, 'A').

    Tests:
        python -m doctest minheap.py
        python test_minheap.py

    """

    def __init__(self, elements=None):
        self.h = []
        # Track current index of labels.
        self.index = {}
        if elements is not None:
            self._heapify(elements)

    def __contains__(self, element):
        return element in self.h

    def __len__(self):
        return len(self.h)

    def __repr__(self):
        return repr(self.h)

    def _label(self, element):
        if isinstance(element, tuple) and len(element) == 2:
            return element[1]
        return element

    def _val(self, element):
        if isinstance(element, tuple) and len(element) == 2:
            return element[0]
        return element

    def _parent_index(self, index):
        return (index - 1) // 2

    def _left_child_index(self, index):
        return (index * 2) + 1

    def _right_child_index(self, index):
        return (index * 2) + 2

    def _heapify(self, elements):
        self.h = []
        for e in elements:
            self.insert(e)

    def _sift_up(self, i=None):
        if i is None:
            i = len(self.h) - 1

        p = self._parent_index(i)

        while p >= 0 and self._val(self.h[p]) > self._val(self.h[i]):
            self.h[i], self.h[p] = self.h[p], self.h[i]
            # Update label indices.
            self.index[self._label(self.h[i])], self.index[self._label(self.h[p])] = (
                self.index[self._label(self.h[p])],
                self.index[self._label(self.h[i])],
            )
            i = p
            p = self._parent_index(i)
        return i

    def _sift_down(self, i=None):
        if i is None:
            i = 0

        while True:
            l = self._left_child_index(i)
            r = self._right_child_index(i)

            smallest = i

            if l < len(self.h) and self._val(self.h[i]) > self._val(self.h[l]):
                smallest = l
            if r < len(self.h) and self._val(self.h[smallest]) > self._val(self.h[r]):
                smallest = r

            if smallest != i:
                self.h[i], self.h[smallest] = self.h[smallest], self.h[i]
                # Update label indices.
                (
                    self.index[self._label(self.h[i])],
                    self.index[self._label(self.h[smallest])],
                ) = (
                    self.index[self._label(self.h[smallest])],
                    self.index[self._label(self.h[i])],
                )
                smallest = i
            else:
                return i

    def is_empty(self):
        return len(self.h) == 0

    def peek(self):
        return self.h[0] if len(self.h) > 0 else None

    @pythoness.spec(
        """Insert unique element into heap.

            Args:
                element: any value. If a two-element tuple i.e. (5, 'A'), the
                the first element t[0] becomes the comparison value and t[1]
                acts as a label.

            Returns:
                Final index of inserted element on the heap array after
                re-heap.

            Raises:
                ValueError: if element already exists in heap.
""",
        related_objs=["cls"],
        tests=[tests],
    )
    def insert(self, element):
        """"""

    @pythoness.spec(
        """Update minimum value of element in heap.

            Args:
                value: Value to overwrite existing value only if it is less
                than the existing value. If not smaller, no change occurs.

                label: Identifying label of element. If a two-element tuple,
                i.e. (5, 'A'), the label is 'A'. Any other value, the label
                is that value, i.e. (1, 1, 1) or 55. Therefore, if original
                element was an integer 10, update_min(5, 10) would replace
                10 in the heap with 5.

            Returns:
                Final element after update.

            Raises:
                ValueError: If element with `label` not found in heap or element
                replacing current element value is already in the heap.
""",
        related_objs=["cls"],
        tests=[tests],
    )
    def update_min(self, value, label):
        """"""

    @pythoness.spec(
        """Remove element with smallest value in heap, then re-heapify heap.

            Returns:
                Element with smallest value in the heap.""",
        related_objs=["cls"],
        tests=[tests],
    )
    def pop(self):
        """"""


if __name__ == "__main__":
    heap = MinHeap([10, 5, 2, 8, -1, 9])
    heap.insert((1, "A"))
    heap.update_min(7, "I")
    print(heap.pop())
