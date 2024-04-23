import unittest

from sympy import symbols
from sympy.logic.boolalg import Not

from Belief import Belief
from BeliefBase import BeliefBase
from Agent import Agent
from Clause import Clause
from Entailment import resolution


class BasicRevisionTests(unittest.TestCase):
    def test_slide_example_robert_exam(self):
        # Test the example from the slides (Robert and the exam)
        beliefs = [Belief('(R >> P | L) & ((P | L) >> R)'), Belief('~R')]
        base = BeliefBase(beliefs)
        print(base)
        clauses = base.clausal_form()
        for clause in clauses:
            print(clause)
        c1 = clauses.pop()
        c2 = clauses.pop()
        res = Clause.resolve(c1, c2)
        if res is not None:
            for r in res:
                print(r)
        # assert resolution(base, ~symbols('P'))
        self.assertTrue(resolution(base, ~symbols('P')))

    def test_case_trivial_clauses(self):
        # Test that after resolving clashing clauses the trivial resolvents are removed
        res = Clause.resolve(
            Clause({'C', 'A', 'B'}),
            Clause({Not('A'), Not('B')}))
        self.assertTrue(len(res) == 0)

    def test_case_from_slides(self):
        # Create the initial belief base in a Agent
        p, q, r = symbols('p, q, r')
        beliefs = [Belief(p), Belief(q), Belief(r)]
        belief_base = BeliefBase(beliefs)
        agent = Agent(belief_base)

        # Absorb new learning
        new_knowledge = ~(q | r)
        new_belief_base = agent.revision(new_knowledge)

        # assert new_belief_base == {p, ~(q | r)}
        new_beliefs = new_belief_base.get_beliefs()
        self.assertIn(p, new_beliefs)
        self.assertIn(~(p | r), new_beliefs)
        self.assertNotIn(q, new_beliefs)
        self.assertNotIn(r, new_beliefs)


