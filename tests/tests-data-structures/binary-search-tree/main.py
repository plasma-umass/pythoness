from util import implementation as i


if __name__ == "__main__":
    bst = i.BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(20)
    bst.insert(40)
    bst.insert(70)
    bst.insert(60)
    bst.insert(80)

    print("In-order traversal:", bst.inorder())  # Output: [20, 30, 40, 50, 60, 70, 80]
    print(
        "Pre-order traversal:", bst.preorder()
    )  # Output: [50, 30, 20, 40, 70, 60, 80]
    print(
        "Post-order traversal:", bst.postorder()
    )  # Output: [20, 40, 30, 60, 80, 70, 50]

    bst.delete(20)

    print(
        "In-order traversal after deleting 20:", bst.inorder()
    )  # Output: [30, 40, 50, 60, 70, 80]

    node = bst.search(70)
    print("Search for 70:", "Found" if node else "Not found")  # Output: Found
