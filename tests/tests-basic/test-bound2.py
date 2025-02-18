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
)
def merge_sort(a: list) -> list:
    """"""


merge_sort([1, 2, 3, 1, 2, 1])
