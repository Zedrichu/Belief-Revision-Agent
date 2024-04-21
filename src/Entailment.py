import copy
from sympy import symbols

from Clause import Clause
from utils import *
from Belief import Belief
from BeliefBase import BeliefBase


def entails(premise_base, statement) -> bool:
    """
    Entailment (BB ⊨ φ) checking using resolution refutation - proving BB ∧ ¬φ is unsatisfiable
    :param premise_base: belief base considered as the premise
    :param statement: statement to be entailed
    :return: boolean value if the statement is entailed by the premise base
    """
    return resolution(premise_base, statement)

"""
Propositional logic resolution pseudoalgorithm

clauses = set of clauses in CNF form of KB and ¬α
new = {}
while True:
    for each pair of clauses Ci, Cj in clauses:
        resolvents = resolve(Ci, Cj)
        if resolvents contains the empty clause:
            return True
        new = new ∪ resolvents
    if new ⊆ clauses:
        return False
    clauses = clauses ∪ new
"""


def resolution(base: BeliefBase, alpha: BooleanFunction):
    """
    Resolution refutation algorithm for propositional logic
    :param base: BeliefBase
    :param alpha: BooleanFunction
    :return: bool
    """
    # Create a new belief base with the premise base and the negation of the formula
    belief_base = copy.copy(base)
    belief_base.add_belief(Belief(~alpha))

    # Split the base into conjunctions of clauses - set of clauses
    clauses = belief_base.clausal_form()

    # Apply resolution refutation
    while True:
        new_clauses = set()
        # Attempt to resolve each pair of clauses
        for clause1 in clauses:
            for clause2 in clauses:
                # Set of all possible resolvents if clauses are clashing
                resolvents = Clause.resolve(clause1, clause2)
                # If the empty clause is found, the formula is entailed (refutation is unsatisfiable)
                if Clause.empty_clause() in resolvents:
                    # Printout for debugging
                    # for r in resolvents:
                    #     print(r)
                    return True
                # Add the resolvents to the new set of clauses
                new_clauses.update(resolvents)
        # No new resolvent were found - formula is not entailed (refutation is satisfiable)
        if new_clauses.issubset(clauses):
            return False
        # Union of the new resolvents with the set of clauses in the base
        clauses.update(new_clauses)


if __name__ == '__main__':
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
    print(resolution(base, ~symbols('P')))
    # Test that the empty clause is found in the set of clauses
    assert Clause.empty_clause() in {Clause.empty_clause()}
    # Test that
    for r in Clause.resolve(Clause({'A', 'B'}), Clause({'A', Not('B')})):
        print(r)
    pass
