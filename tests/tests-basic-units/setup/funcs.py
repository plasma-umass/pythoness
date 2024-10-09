from . import tests
import pythoness
import unittest


@pythoness.spec(
    "Returns str but all lowercase letters become uppercase letters", tests=[]
)
def upper(string: str) -> str:
    """"""


@pythoness.spec(
    "Returns True when str is only composed of uppercase characters",
    max_retries=6,
    tests=[tests.TestStringMethods],
)
def isupper(string: str) -> bool:
    """"""


@pythoness.spec(
    "Returns a list of substrings in str using sep as the separator string",
    tests=[tests],
)
def split(string: str, sep: str) -> list:
    """"""


if __name__ == "__main__":
    print(upper.__module__)
