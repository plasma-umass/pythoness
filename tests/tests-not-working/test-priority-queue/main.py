from setup import priority_queue as prq

if __name__ == "__main__":
    pq = prq.PriorityQueue()

    pq.add(3, 4)
    pq.add(1, 2)
    pq.add(2, 9)

    print(pq.pop())
    print(pq.pop())
    print(pq.peek())
    print(pq.pop())
    print(pq.peek())
