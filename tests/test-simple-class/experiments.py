import pythoness

def func(str):
    "text"
    return None

def func2(str):
    return True

class Superclass:
    ""

class Class(Superclass):
    def func3(input):
        return False

@pythoness.spec("adds two numbers", related_objs = ['cls', 'cls'])
def add(a, b):
    ""

if __name__ == "__main__":
    print(Class.__bases__)