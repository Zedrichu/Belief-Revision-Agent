import unittest

from src.Agent import Agent
from src.Belief import Belief
from src.BeliefBase import BeliefBase


class RevisionTests(unittest.TestCase):
    def test_case_from_slides(self):
        # Lecture 9 page 32
        belief_base = BeliefBase([Belief('p'), Belief('q'), Belief('r')])
        sut = Agent(belief_base)

        new_beliefs = sut.revision('~(q | r)').get_beliefs()

        self.assertIn(Belief('p'), new_beliefs)
        self.assertIn(Belief('~(q | r)'), new_beliefs)
        self.assertNotIn(Belief('q'), new_beliefs)
        self.assertNotIn(Belief('r'), new_beliefs)

    def test_basic_revision(self):
        # Example - lecture 9 page 35
        initial_beliefs = BeliefBase([Belief('p'), Belief('q'), Belief('p >> q')])

        sut = Agent(initial_beliefs)
        new_beliefs = sut.revision('~q').get_beliefs()

        self.assertIn(Belief('p'), new_beliefs)
        self.assertIn(Belief('~q'), new_beliefs)
        self.assertNotIn(Belief('q'), new_beliefs)
        self.assertNotIn(Belief('p >> q'), new_beliefs)

    def test_basic_contradiction(self):
        initial_beliefs = BeliefBase([Belief('p')])

        sut = Agent(initial_beliefs)
        new_beliefs = sut.revision('~p').get_beliefs()

        self.assertIn(Belief('~p'), new_beliefs)
