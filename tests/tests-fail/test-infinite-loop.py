import pythoness

@pythoness.spec("A function that never terminates", timeout_seconds=10)

def infinite():
    ""

infinite()