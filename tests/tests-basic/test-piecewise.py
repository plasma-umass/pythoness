import pythoness


@pythoness.spec(
    "Given an int x, return 2x if x is negative, return 3x if x is positive.",
    output=True,
    verbose=True,
    tests=[
        "piecewise(6) == 18",
        "piecewise(-3) == -6",
        ({"x": "integers(-20,0)"}, "piecewise(x) == 2 * x"),
        ({"x": "integers(0,20)"}, "piecewise(x) == 3 * x"),
    ],
)
def piecewise(x: int) -> int:
    """"""


for i in range(-100, 0):
    assert piecewise(i) == 2 * i
for i in range(0, 101):
    assert piecewise(i) == 3 * i
print("All tests passed!")
