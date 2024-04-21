import copy

from sympy import symbols
from sympy.logic.boolalg import *

from Clause import Clause
from utils import *
from Belief import Belief
from BeliefBase import BeliefBase


def entails(premise_base, statement):
    """
    Entailment (BB ⊨ φ) checking using resolution refutation - proving BB ∧ ¬φ is unsatisfiable
    :param premise_base:
    :param statement:
    :return:
    """
    # Create a new belief base with the premise base and the negation of the formula
    belief_base = premise_base.copy()
    belief_base.add(~statement)

    # Split base into conjunctions of clauses
    clauses = set()
    for belief in belief_base.beliefs:
        clauses.add(belief.formula)


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
        for clause1 in clauses:
            for clause2 in clauses:
                resolvents = Clause.resolve(clause1, clause2)
                if resolvents is None:
                    return True
                new_clauses.update(resolvents)
        if new_clauses.issubset(clauses):
            return False
        clauses.update(new_clauses)


if __name__ == '__main__':
    beliefs = [Belief('A'), Belief('~B'), Belief('C >> B'), Belief('A >> C')]
    base = BeliefBase(beliefs)
    print(base)
    clauses = base.clausal_form()
    for clause in clauses:
        print(clause)
    c1 = clauses.pop()
    c2 = clauses.pop()
    res = Clause.resolve(c1, c2)
    if res is not None:
        print(res)
    print(resolution(base, symbols('A')))
    pass
