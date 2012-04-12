from nose2.compat import unittest
from nose2.tools import params


def tests_can_be_functions():
    assert True


def tests_can_be_generators():
    def check(val):
        assert val == val, "Identity failure!"
    for i in range(1, 4):
        yield check, i


@params(1, 2, 3)
def tests_can_take_parameters(p):
    assert p < 4, "How'd that get here?"


class TestsCanBeUnittestTestCases(unittest.TestCase):
    def setUp(self):
        self.x = 1

    def test_one(self):
        self.assertEqual(self.x, 1)


class TestsCanBePlainClasses(object):
    def setUp(self):
        self.me_too = 1

    def test(self):
        assert self.me_too == 1, "Not me too?"
