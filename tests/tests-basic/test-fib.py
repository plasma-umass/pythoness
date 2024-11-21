import pythoness


@pythoness.spec(
    "Compute the nth number in the Fibonacci series.",
    tests=[
        "myfib(0) == 0",
        "myfib(1) == 1",
        ("n>0", "myfib(n+2) == myfib(n+1)+myfib(n)"),
    ],
    test_descriptions=[
        "myfib(n) should be the sum of calling myfib on the previous 2 numbers",
        "myfib(n) should produce a positive integer",
    ],
    max_retries=3,
    exec=True,
    regenerate=True,
    verbose=True,
)
def myfib(n: int) -> int:
    """"""


for i in range(20):
    print(myfib(i))
