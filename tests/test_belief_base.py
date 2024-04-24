import unittest

from Belief import Belief
from BeliefBase import BeliefBase
from Entailment import entails


class BeliefBaseTests(unittest.TestCase):
    def test_resolution_basic_contradiction(self):
        sut = BeliefBase([Belief('p'), Belief('~p')])
        actual = sut.resolution()
        self.assertTrue(actual)

    def test_resolution_with_no_contradiction(self):
        sut = BeliefBase([Belief('p | q')])
        actual = sut.resolution()
        self.assertFalse(actual)

    def test_entails(self):
        self.assertTrue(entails(BeliefBase([]), 'p | ~p'))
