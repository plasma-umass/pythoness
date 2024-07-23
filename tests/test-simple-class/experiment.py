import inspect
import pythoness

def d(a):
    ""

class A:
    class B:
        def c():
            ""

@pythoness.spec("adds a and b")
def add(a, b):
    ""

    
@pythoness.spec("adds a, b, and c", related_objs=[add])
def add3(a, b, c):
    ""


if __name__ == "__main__":
    # print(inspect.isfunction.__qualname__)
    # print(inspect.getmodule(inspect.isfunction).__name__)
    # print(inspect.getmodule(d).__name__)
    # print(inspect.signature(d))
    print(add3(3, 1, 1))
