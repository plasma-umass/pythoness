import pythoness
import random
import numpy as np


def random_array(n):
    return np.array([random.randint(0, 100) for _ in range(n)])


@pythoness.spec(
    "Reverse the array",
    tests=[],
    test_descriptions=[],
    max_retries=3,
    mem_bound="O(1)",
    length_func=lambda n: len(n),
    generate_func=lambda n: ([random_array(n)], {}),
    range=(0, 50000),
    regenerate=True,
    verbose=True,
)
def reverse(a: np.ndarray) -> np.ndarray:
    """"""


reverse(random_array(10))
