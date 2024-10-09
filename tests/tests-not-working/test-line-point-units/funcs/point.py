import pythoness
from . import tests

# ISSUE: it's adding functions to the globals and there's too many functions in the prompt
# TODO: when I generate the __init__ function it's being added to the globals
# I'm throwing the funtion into globals and then accessing it from there later


class Point:
    """A 2D point"""

    @pythoness.spec("initializes an x coord and a y coord", tests=[tests.TestInit])
    def __init__(self, x: int, y: int):
        """"""

    @pythoness.spec(
        "Formats the point object's string, s.t. it looks like a typical coordinate pair (x, y)",
        related_objs=[__init__],
        tests=[tests.TestStr],
    )
    def __str__(self):
        """"""

    @pythoness.spec(
        "compares two points s.t. if the coords in each object are identical, __eq__ returns True",
        related_objs=["cls"],
        tests=[tests.TestEq],
    )
    def __eq__(self, other):
        """"""

    @pythoness.spec(
        "Gets the x coord from the point.",
        related_objs=[__init__],
        tests=[tests.TestGetX],
    )
    def get_x(self):
        """"""

    @pythoness.spec(
        "Gets the y coord from the point.",
        related_objs=[__init__],
        tests=[tests.TestGetY],
    )
    def get_y(self):
        """"""

    @pythoness.spec(
        "Sets the x coord of the point, then returns the point",
        related_objs=[__init__],
        tests=[tests.TestSetX],
    )
    def set_x(self, y: int):
        """"""

    @pythoness.spec(
        "Sets the y coord of the point, then returns the point",
        related_objs=[__init__],
        tests=[tests.TestSetY],
    )
    def set_y(self, x: int):
        """"""

    @pythoness.spec(
        "Transposes the x coord by x_trans and the y coord by y_trans",
        related_objs=["cls"],
        tests=[tests.TestTranspose],
    )
    def transpose(self, x_trans: int, y_trans: int):
        """"""
