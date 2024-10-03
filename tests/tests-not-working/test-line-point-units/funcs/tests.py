import unittest
from . import point as p
from . import line as l


class TestInit(unittest.TestCase):

    def test_init(self):
        point = p.Point(1, 2)
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)


class TestStr(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(p.Point(1, 1)), "(1,1)")


class TestEq(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(p.Point(1, 1), p.Point(1, 1))


class TestGetX(unittest.TestCase):

    def test_get_x(self):
        self.assertEqual(p.Point(1, 1).get_x(), 1)


class TestGetY(unittest.TestCase):

    def test_get_y(self):
        self.assertEqual(p.Point(1, 2).get_y(), 2)


class TestSetX(unittest.TestCase):

    def test_set_x(self):
        point = p.Point(1, 1)
        point.set_x(3)

        self.assertEqual(p.Point(3, 1), point)


class TestSetY(unittest.TestCase):

    def test_set_y(self):
        point = p.Point(1, 1)
        point.set_y(3)

        self.assertEqual(p.Point(1, 3), point)


class TestTranspose(unittest.TestCase):

    def test_transpose(self):
        point = p.Point(1, 1)
        point.transpose(1, -1)

        self.assertEqual(p.Point(2, 0), point)


class TestLineInit(unittest.TestCase):

    def test_init(self):
        line = l.Line(p.Point(1, 1), p.Point(2, 2))

        self.assertEqual(line.p1, p.Point(1, 1))
        self.assertEqual(line.p2, p.Point(2, 2))


class TestLineEq(unittest.TestCase):

    def test_eq(self):

        self.assertEqual(
            l.Line(p.Point(1, 1), p.Point(1, 2)), l.Line(p.Point(1, 1), p.Point(1, 2))
        )
        self.assertNotEqual(
            l.Line(p.Point(1, 1), p.Point(1, 3)), l.Line(p.Point(1, 1), p.Point(1, 2))
        )


class TestLineAdd(unittest.TestCase):

    def test_add(self):

        self.assertEqual(
            l.Line(p.Point(1, 1), p.Point(1, 2)) + l.Line(p.Point(1, 1), p.Point(1, 2)),
            l.Line(p.Point(2, 2), p.Point(2, 4)),
        )


class TestLineStr(unittest.TestCase):

    def test_str(self):

        self.assertEqual(str(l.Line(p.Point(1, 1), p.Point(1, 2))), "((1,1), (1,2))")


class TestLineGetP1(unittest.TestCase):

    def test_get_p1(self):

        self.assertEqual(l.Line(p.Point(1, 1), p.Point(1, 2)).get_p1(), p.Point(1, 1))


class TestLineGetP2(unittest.TestCase):

    def test_get_p1(self):

        self.assertEqual(l.Line(p.Point(1, 1), p.Point(1, 2)).get_p2(), p.Point(1, 2))
