import pythoness

@pythoness.spec("Given a string s and a character c, return the number of times c appears in s.")
def count_chars(s: str, c: str) -> int:
    ""


assert(count_chars("hello, this is a test.", "t") == 3)
assert(count_chars("hello, this is a test.", "e") == 2)
assert(count_chars("hello, this is a test.", "s") == 3)
assert(count_chars("hello, this is a test.", "i") == 2)
assert(count_chars("hello, this is a test.", "q") == 0)
