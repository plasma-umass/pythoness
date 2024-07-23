import pythoness
import test_point
import inspect

def a(b):
    ""

class Line:
    "A basic 2D line class"

    @pythoness.spec("initializes a line, which is composed of two points", related_objs=[test_point.Point])
    def __init__(self, p1, p2):
        ""

    def __eq__(self, other):
        return self.p1.x == other.p1.x and self.p1.y == other.p1.y and self.p2.x == other.p2.x and self.p2.y == other.p2.y 

    @pythoness.spec("adds two lines by adding the corrsponding values of each point, (x1 + x2, y1 + y2)", related_objs=['cls', test_point.Point], tests=["Line(test_point.Point(1,1), test_point.Point(1,1)) + Line(test_point.Point(1,1), test_point.Point(1,1)) == Line(test_point.Point(2,2), test_point.Point(2,2)) "])
    def __add__(self, other):
        ""

    def __str__(self):
        return f'{(str(self.p1), str(self.p2))}'
    

@pythoness.spec("adds two points, s.t. the corresponding coords are added", related_objs=[test_point.Point])    
def add_two_points(p1 : test_point.Point, p2 : test_point.Point) -> test_point.Point:
    ""

@pythoness.spec("gets the signature of a function and converts it to a string", tests=["get_function_string(a) == '(b)'"])
def get_function_string(func):
    pass


if __name__ == "__main__":
    line1 = Line(test_point.Point(1,2), test_point.Point(3, 2))
    line2 = Line(test_point.Point(-1, -2), test_point.Point(-3, -2))
    print(line1 + line2)
    p1 = test_point.Point(1,1)
    p2 = test_point.Point(1,1)
    print(add_two_points(p1, p2))
    print(get_function_string(a))