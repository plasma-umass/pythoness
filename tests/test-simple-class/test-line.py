import pythoness
import test_point
import inspect

def a(b):
    """"""

class Line:
    """A basic 2D line class"""

    @pythoness.spec("initializes a line, which is composed of two points, p1 and p2", related_objs=[test_point.Point])
    def __init__(self, p1, p2):
        ""

    @pythoness.spec('returns True if all coords of points are equal, false otherwise', tests=['Line(test_point.Point(1,1), test_point.Point(1,1)) == Line(test_point.Point(1,1), test_point.Point(1,1))', 'Line(test_point.Point(1,1), test_point.Point(1,1)) != Line(test_point.Point(2,1), test_point.Point(1,1))'], related_objs=['cls', test_point.Point])
    def __eq__(self, other):
        ""

    @pythoness.spec("adds two lines by adding the corrsponding values of each point, (x1 + x2, y1 + y2)", related_objs=['cls', test_point.Point], tests=["Line(test_point.Point(1,1), test_point.Point(1,1)) + Line(test_point.Point(1,1), test_point.Point(1,1)) == Line(test_point.Point(2,2), test_point.Point(2,2))"])
    def __add__(self, other):
        ""

    @pythoness.spec('converts the line into the form (p1, p2)', related_objs=['cls', test_point.Point], tests=["str(Line(test_point.Point(1,1), test_point.Point(1,1))) == '((1,1), (1,1))'"])
    def __str__(self):
        ""

    @pythoness.spec('gets p1 in the line', related_objs=[__init__], tests=["Line(test_point.Point(1,1), test_point.Point(2,2)).get_p1() == test_point.Point(1,1)"])
    def get_p1(self):
        ""

    @pythoness.spec('gets p2 in the line', related_objs=[__init__], tests=["Line(test_point.Point(1,1), test_point.Point(2,2)).get_p2() == test_point.Point(2,2)"])
    def get_p2(self):
        ""

if __name__ == '__main__':
    line1 = Line(test_point.Point(1, 2), test_point.Point(3, 2))
    line2 = Line(test_point.Point(-1, -2), test_point.Point(-3, -2))
    line3 = line1 + line2
    print(line3)