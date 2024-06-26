import pythoness

@pythoness.spec("Given a string s and a character c, return the number of times c appears as a consecutive pair in s.",
                tests = ["count_chars('hello', 'e') == 0",
                         "count_chars('hello', 'l') == 1",
                         "count_chars('helll', 'l') == 2",
                         "count_chars('what is up', 'q') == 0"])

def count_chars(s: str, c) -> int:
    ""

print("Running tests: count-all-characters-twice")
assert(count_chars("hello, this is a test.", "t") == 0)
assert(count_chars("hello, this is a test.", "e") == 0)
assert(count_chars("hello, this is a test.", "s") == 0)
assert(count_chars("hello, this is a test.", "l") == 1)
assert(count_chars("hello, this is a test.", "q") == 0)
print("Tests complete.")