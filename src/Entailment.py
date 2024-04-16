from sympy.logic.boolalg import *

def entails(premise_base, formula):
    """
    Entailment (BB ⊨ φ) checking using resolution refutation - proving BB ∧ ¬φ is unsatisfiable
    :param premise_base:
    :param formula:
    :return:
    """
    # Create a new belief base with the premise base and the negation of the formula
    belief_base = premise_base.copy()
    belief_base.add(~formula)

    # Split base into conjuctions of clauses
    clauses = set()
    for belief in belief_base.beliefs:
        clauses.add(belief.formula)

