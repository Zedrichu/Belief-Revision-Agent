import unittest

from sympy import symbols

from Belief import Belief
from BeliefBase import BeliefBase
from Agent import Agent


class BasicRevisionTests(unittest.TestCase):
    def test_some_bullshit_basic_case(self):
        initial_beliefs = []
        new_beliefs = []

        # revised_beliefs = revise(initial_beliefs, new_beliefs)
        # assert revised_beliefs contains ...

    def test_case_from_slides(self):
        # Create the initial belief base in a Agent
        p, q, r = symbols('p, q, r')
        beliefs = {Belief(p), Belief(q), Belief(r)}
        belief_base = BeliefBase(beliefs)
        agent = Agent(belief_base)

        # Do new learning
        new_knowledge = ~(q | r)
        new_belief_base = agent.revision(agent.belief_base, new_knowledge)

        # assert new_belief_base == {p, ~(q | r)}
        self.assertIn(p, new_belief_base.beliefs)
        self.assertIn(~(p | r), new_belief_base.beliefs)
        self.assertNotIn(q, new_belief_base.beliefs)
        self.assertNotIn(r, new_belief_base.beliefs)
