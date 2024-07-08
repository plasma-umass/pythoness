import inspect
import textwrap

def test_func():
    """Runs a test"""

def explode(a, b : float, c : int = 1, d="a"):
    "Boom"

def get_docstring(test_func):
    print(inspect.getdoc(test_func))

# get_docstring(test_func)

def get_docstrings(related_funcs : list):
    str = """
            Below is a list of functions that may be used in the implementation.
            Included is their name, signature, and docstring.
        """
    for func in related_funcs:
        str += f"""
                {func.__name__}{inspect.signature(func)}:
                    '''{inspect.getdoc(func)}'''
                """
    return str

print(get_docstrings([test_func, explode]))

