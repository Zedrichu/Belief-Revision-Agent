import unittest

from AGMPostulates import AGMPostulates
from Belief import Belief
from BeliefBase import BeliefBase


class AgmPostulatesTests(unittest.TestCase):
    def test_vacuity_1(self):
        belief_base = BeliefBase([Belief('p'), Belief('q'), Belief('p >> q')])

        actual = AGMPostulates.vacuity(belief_base, '~p')

        self.assertTrue(actual)

    def test_consistency(self):
        belief_base = BeliefBase([Belief('p'), Belief('q'), Belief('p >> q')])

        actual = AGMPostulates.consistency(belief_base, '~p')

        self.assertTrue(actual)