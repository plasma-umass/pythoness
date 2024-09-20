import heapq
import pythoness
from collections import Counter
# Node class for the Huffman Tree

class Node:

    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    # To compare nodes for priority queue

    def __lt__(self, other):
        return self.freq < other.freq
# Function to build the Huffman Tree

def build_huffman_tree(frequency):
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)
    return heap[0]
# Function to build the Huffman Code from the tree

def build_huffman_code(root):
    huffman_code = {}

    def build_code_helper(node, current_code):
        if node is None:
            return
        if node.char is not None:
            huffman_code[node.char] = current_code
        build_code_helper(node.left, current_code + '0')
        build_code_helper(node.right, current_code + '1')
    build_code_helper(root, '')
    return huffman_code
# Function to encode the input text using the Huffman Code

def encode(input_string):
    if not input_string:
        return ('', {})
    # Step 1: Calculate frequency of each character
    frequency = Counter(input_string)
    # Step 2: Build Huffman Tree
    huffman_tree_root = build_huffman_tree(frequency)
    # Step 3: Build Huffman Code from the tree
    huffman_code = build_huffman_code(huffman_tree_root)
    # Step 4: Encode the input string
    encoded_string = ''.join((huffman_code[char] for char in input_string))
    return (encoded_string, huffman_code)

import heapq
from collections import defaultdict

class Node:

    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def decode(str, tr):
    """
    Decode str into the string inputted into an encode() function.
    Here is a sample input and output to the encode() function:
    encode('hello, world!') == '000001010111010111111111011010000110011010', and here
    is the Node class:
    class Node:
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # To compare nodes for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

    Arguments: [['Name: str', "Type: <class 'str'>"], ['Name: tr', "Type: <class '__main__.Node'>"]]
    Return type: <class 'str'>
    """
    current_node = tr
    decoded_string = ''
    for bit in str:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.left is None and current_node.right is None:
            decoded_string += current_node.char
            current_node = tr
    return decoded_string

# Test the function
test_string = 'awhiodajoifhwa'
frequency = Counter(test_string)
tr = build_huffman_tree(frequency)
encoded_string, hc = encode(test_string)
decoded_string = decode(encoded_string, tr)
print(f'Original: {test_string}')
print(f'Encoded: {encoded_string}')
print(f'Huffman Code: {hc}')
print(f'Decoded: {decoded_string}')