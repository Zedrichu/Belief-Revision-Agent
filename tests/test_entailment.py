import unittest

from sympy import symbols
from sympy.logic.boolalg import Not

from Belief import Belief
from BeliefBase import BeliefBase
from Agent import Agent
from Clause import Clause
from Entailment import entails


class BasicRevisionTests(unittest.TestCase):
    def test_slide_example_robert_exam(self):
        # Test the example from the slides (Robert and the exam)
        beliefs = [Belief('(R >> P | L) & ((P | L) >> R)'), Belief('~R')]
        base = BeliefBase(beliefs)
        clauses = base.clausal_form()
        c1 = clauses.pop()
        c2 = clauses.pop()
        res = Clause.resolve(c1, c2)
        self.assertTrue(entails(base, '~P'))

    def test_case_trivial_clauses(self):
        # Test that after resolving clashing clauses the trivial resolvents are removed
        res = Clause.resolve(
            Clause({'C', 'A', 'B'}),
            Clause({Not('A'), Not('B')}))
        self.assertTrue(len(res) == 0)

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
        # Lecture 9 page 35
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
