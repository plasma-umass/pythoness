import unittest
from . import funcs

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertNotEqual(funcs.upper('foo'), 'FOO')
        
    def test_isupper(self):
        self.assertTrue(funcs.isupper('FOO'))
        self.assertFalse(funcs.isupper('Foo'))

    def test_split(self):
        s = 'hello world'
        self.assertEqual(funcs.split(s, ' '), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            funcs.split(2, ' ')

class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6, 2):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

