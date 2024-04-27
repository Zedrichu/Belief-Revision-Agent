import unittest

from src.AGMPostulates import AGMPostulates
from src.Belief import Belief
from src.BeliefBase import BeliefBase


class AgmPostulatesTests(unittest.TestCase):
    def test_inclusion_on_empty_belief_base(self):
        belief_base = BeliefBase([])
        self.assertTrue(AGMPostulates.inclusion(belief_base, 'p'))

    def test_inclusion_with_a_phi_negating_existing_belief(self):
        belief_base = BeliefBase([Belief('p')])
        self.assertTrue(AGMPostulates.inclusion(belief_base, '~p'))

    def test_vacuity(self):
        belief_base = BeliefBase([Belief('p'), Belief('q')])
        self.assertTrue(AGMPostulates.vacuity(belief_base, 'p'))

    def test_vacuity_when_negated_phi_exists_in_belief_base(self):
        belief_base = BeliefBase([Belief('p'), Belief('q')])
        self.assertTrue(AGMPostulates.vacuity(belief_base, '~p'))

    def test_vacuity_on_empty_belief_base(self):
        belief_base = BeliefBase([])
        self.assertTrue(AGMPostulates.vacuity(belief_base, 'p'))

    def test_consistency(self):
        belief_base = BeliefBase([Belief('p'), Belief('q')])
        self.assertTrue(AGMPostulates.consistency(belief_base, '~p'))

    def test_consistency_when_phi_is_inconsistent(self):
        belief_base = BeliefBase([Belief('p'), Belief('q')])
        self.assertTrue(AGMPostulates.consistency(belief_base, 'p & ~p'))

    def test_consistency_on_empty_belief_base(self):
        belief_base = BeliefBase([])
        self.assertTrue(AGMPostulates.consistency(belief_base, 'p'))

    def test_extensionality_on_non_equivalent(self):
        belief_base = BeliefBase([Belief('p'), Belief('q')])
        self.assertTrue(AGMPostulates.extensionality(belief_base, phi='p', psi='q'))

    def test_extensionality_on_non_equivalent_with_empty_belief_base(self):
        belief_base = BeliefBase([])
        self.assertTrue(AGMPostulates.extensionality(belief_base, phi='p', psi='q'))

    def test_extensionality_on_equivalent_with_empty_belief_base(self):
        belief_base = BeliefBase([])
        self.assertTrue(AGMPostulates.extensionality(belief_base, phi='p >> q', psi='~p | q'))

    def test_extensionality_on_equivalent(self):
        belief_base = BeliefBase([Belief('p')])
        self.assertTrue(AGMPostulates.extensionality(belief_base, phi='p >> q', psi='~p | q'))
