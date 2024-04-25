import unittest

from sympy.logic.boolalg import Not

from Belief import Belief
from BeliefBase import BeliefBase
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
