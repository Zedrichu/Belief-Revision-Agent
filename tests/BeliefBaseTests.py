import unittest

from Belief import Belief
from BeliefBase import BeliefBase
from Entailment import entails


class BeliefBaseTests(unittest.TestCase):
    def test_foo(self):
        sut = BeliefBase([Belief('p'), Belief('~p')])
        actual = sut.resolution()
        self.assertTrue(actual)

    def test_bar(self):
        sut = BeliefBase([Belief('p | q')])
        actual = sut.resolution()
        self.assertFalse(actual)

    def test_for(self):
        assert entails(BeliefBase([]), 'p | ~p')
