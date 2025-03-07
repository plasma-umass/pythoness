import pythoness


@pythoness.spec(
    "Compute the nth number in the Fibonacci series.  Write the recursive exponential time version",
    max_retries=3,
    time_bound="O(n)",
    length_func=lambda n: int(n),
    generate_func=lambda n: ([int(n)], {}),
    range=(0, 25),
    regenerate=True,
    verbose=True,
    pure=False,
    runtime=True
)
def myfib(n: int) -> int:
    """"""


for i in range(20):
    print(i)
    print(myfib(i))
