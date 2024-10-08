import pythoness

# ISSUE: it's adding functions to the globals and there's too many functions in the prompt
# TODO: when I generate the __init__ function it's being added to the globals
# I'm throwing the funtion into globals and then accessing it from there later


class Point:
    """A 2D point"""

    @pythoness.spec("initializes an x coord and a y coord")
    def __init__(self, x: int, y: int):
        """"""

    @pythoness.spec(
        "Formats the point object's string, s.t. it looks like a typical coordinate pair (x, y)",
        related_objs=[__init__],
        tests=["str(Point(1,1))=='(1,1)'"],
    )
    def __str__(self):
        """"""

    @pythoness.spec(
        "compares two points s.t. if the coords in each object are identical, __eq__ returns True",
        related_objs=["cls"],
        tests=["Point(1,1) == Point(1,1)"],
    )
    def __eq__(self, other):
        """"""

    @pythoness.spec(
        "Gets the x coord from the point.",
        related_objs=[__init__],
        tests=["Point(1,1).get_x()==1", "test_set_x(Point(1,1))"],
    )
    def get_x(self):
        """"""

    @pythoness.spec(
        "Gets the y coord from the point.",
        related_objs=[__init__],
        tests=["Point(1,1).get_y()==1", "test_set_y(Point(1,1))"],
    )
    def get_y(self):
        """"""

    @pythoness.spec(
        "Sets the x coord of the point, then returns the point", related_objs=[__init__]
    )
    def set_x(self, y: int):
        """"""

    @pythoness.spec(
        "Sets the y coord of the point, then returns the point", related_objs=[__init__]
    )
    def set_y(self, x: int):
        """"""

    @pythoness.spec(
        "Transposes the x coord by x_trans and the y coord by y_trans",
        related_objs=["cls"],
        tests=["test_transpose(Point(1,1))"],
    )
    def transpose(self, x_trans: int, y_trans: int):
        """"""


def test_transpose(point):
    orig_point = point
    point.transpose(3, -1)
    orig_point.set_x(orig_point.get_x() + 3)
    orig_point.set_y(orig_point.get_y() - 1)
    return orig_point == point


def test_set_x(point):
    original_point = point
    point.set_x(1)
    return original_point.set_x(1) == point


def test_set_y(point):
    original_point = point
    point.set_y(1)
    return original_point.set_y(1) == point


if __name__ == "__main__":
    point = Point(1, 1)
    point.transpose(3, -1)
    print(f"({point})")
