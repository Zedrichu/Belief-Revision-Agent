import unittest

from Belief import Belief
from BeliefBase import BeliefBase


class BeliefBaseTests(unittest.TestCase):
    def test_foo(self):
        sut = BeliefBase([Belief('p'), Belief('~p')])
        actual = sut.resolution()
        self.assertTrue(actual)
