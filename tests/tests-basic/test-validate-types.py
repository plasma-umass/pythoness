import pythoness

@pythoness.spec("""Takes a list as an input and returns a new list of equal length where each item is 
           converted into a new type (float, int, string) depending on its original type,
           where floats becomes truncated ints, ints become floats, and strings become None""", 
            tests=["weird_convert([1,2.5,'word']) == [1.0, 2, None]"])

def weird_convert(lst):
    ""

weird_convert([])
