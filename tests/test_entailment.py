import unittest

from sympy.logic.boolalg import Not

from src.Belief import Belief
from src.BeliefBase import BeliefBase
from src.Clause import Clause
from src.Resolution import resolution


class BasicRevisionTests(unittest.TestCase):
    def test_slide_example_robert_exam(self):
        # Test the example from the slides (Robert and the exam)
        beliefs = [Belief('(R >> P | L) & ((P | L) >> R)'), Belief('~R')]
        base = BeliefBase(beliefs)
        clauses = base.clausal_form()
        c1 = clauses.pop()
        c2 = clauses.pop()
        res = Clause.resolve(c1, c2)
        self.assertTrue(base.entails('~P'))

    def test_case_trivial_clauses(self):
        # Test that after resolving clashing clauses the trivial resolvents are removed
        res = Clause.resolve(
            Clause({'C', 'A', 'B'}),
            Clause({Not('A'), Not('B')}))
        self.assertTrue(len(res) == 0)

    def test_resolution_basic_contradiction(self):
        sut = BeliefBase([Belief('p'), Belief('~p')])
        actual = resolution(sut.clausal_form())
        self.assertTrue(actual)

    def test_resolution_with_no_contradiction(self):
        sut = BeliefBase([Belief('p | q')])
        actual = resolution(sut.clausal_form())
        self.assertFalse(actual)

    def test_entails_for_an_empty_belief_base(self):
        self.assertTrue(BeliefBase([]).entails('p | ~p'))

    def test_entails_for_a_contradiction(self):
        self.assertFalse(BeliefBase([Belief('p')]).entails('~p'))

    def test_entails_for_non_existing_beliefs(self):
        self.assertFalse(BeliefBase([Belief('p')]).entails('q'))

    def test_entails_for_a_simple_relationship(self):
        self.assertTrue(BeliefBase([Belief('p'), Belief('p >> q')]).entails('q'))

    def test_entails_for_on_an_empty_belief_base_with_an_inconsistent_belief(self):
        self.assertFalse(BeliefBase([]).entails('p & ~p'))

    def test_entails_for_on_an_empty_belief_base_with_a_negated_inconsistent_belief(self):
        self.assertTrue(BeliefBase([]).entails('~(p & ~p)'))

    def test_entails_for_on_an_empty_belief_base_with_a_consistent_negated_belief(self):
        self.assertFalse(BeliefBase([]).entails('~(p | ~p)'))
