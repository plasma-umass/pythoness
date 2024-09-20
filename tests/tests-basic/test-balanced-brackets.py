import pythoness

@pythoness.spec("""Given a string str return True when str is a string of properly nested and matched
                parens, brackets, and braces and False otherwise. An empty string should return True.""",
                tests=["is_balanced('[]') == True", "is_balanced('[{()}]') == True",
                       "is_balanced('[{)}]') == False", "is_balanced('') == True"])

def is_balanced(str : str) -> bool:
    ""

print("Running tests: balanced-brackets")
assert(is_balanced("[[([{}])]]") == True)
assert(is_balanced("[{(([))}]") == False)
assert(is_balanced("}") == False)
assert(is_balanced("()") == True)
print("Tests complete.")