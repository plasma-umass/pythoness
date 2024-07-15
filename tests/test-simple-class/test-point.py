import pythoness

# ISSUE: it's adding functions to the globals and there's too many functions in the prompt
# TODO: when I generate the __init__ function it's being added to the globals
# I'm throwing the funtion into globals and then accessing it from there later


class Point:
    """A 2D point, (self.x, self.y)"""

    @pythoness.spec("Initializes the point object with an x coord and a y coord. DO NOT write the point class", verbose = True, e_print=True)
    def __init__(self, x: int, y: int):
        ""

    # @pythoness.spec("Formats the point object's string, s.t. it looks like a typical coordinate pair (x, y). Do not write the Point class", verbose = True, e_print=True, related_objs = '*')
    def __str__(self):
        """Formats the point object's string, s.t. it looks like a typical coordinate pair (x, y). Do not write the Point class"""
        return f'({self.get_x()}, {self.get_y()})'

    @pythoness.spec('Gets the x coord from the point. Do NOT define the point class.', verbose=True, e_print=True, related_objs = '*', replace = True)
    def get_x(self):
        ""
 
    @pythoness.spec('Gets the y coord from the point.', verbose = True, e_print=True, related_objs = '*')
    def get_y(self):
        ""

    @pythoness.spec("Sets the y coord of the point", verbose = True, e_print=True, related_objs = '*')
    def set_y(self, x : int):
        ""
 
    @pythoness.spec("Sets the x coord of the point", verbose = True, e_print=True, related_objs = '*')
    def set_x(self, y : int):
        ""
 
    @pythoness.spec("Transposes the x coord by x_trans and the y coord by y_trans, do NOT define a separate class", verbose = True, e_print=True, related_objs = '*',)
    def transpose(self, x_trans : int, y_trans : int):
        ""

class Test:
    def test_func(point : Point):
        point.get_x()

# @pythoness.spec("transposes p's x coords by x and y coords by y", verbose=True, related_objs=[Point])
# def transpose(p : Point, x : int, y : int) -> Point:
#     ""

if __name__ == '__main__':
    point = Point(1, 1)
    point.transpose(3, -1)
    print(f"({point})")