import pythoness
import random


def random_array(n):
    return [random.randint(0, 100) for _ in range(n)]


@pythoness.spec(
    "Merge sort the array",
    tests=[],
    test_descriptions=[],
    max_retries=3,
    time_bound="O(n*log(n))",
    mem_bound="O(n)",
    length_func=lambda n: len(n),
    generate_func=lambda n: ([random_array(n)], {}),
    range=(0, 5000),
    regenerate=True,
    verbose=True,
    runtime=True,
    pure=False  # stop making tests!
)
def merge_sort(a: list) -> list:
    """"""



for i in range(100):
    print(i)
    merge_sort(random_array(random.randint(0, 5000)))
