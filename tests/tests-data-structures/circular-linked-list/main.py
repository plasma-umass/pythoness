from util import implementation as i

# Example usage
if __name__ == "__main__":
    cll = i.CircularLinkedList()
    cll.append(1)
    cll.append(2)
    cll.append(3)
    cll.prepend(0)

    print("Circular Linked List:")
    cll.print_list()  # Output: 0 1 2 3

    cll.delete(2)
    print("After deleting 2:")
    cll.print_list()  # Output: 0 1 3

    cll.delete(0)
    print("After deleting 0:")
    cll.print_list()  # Output: 1 3
