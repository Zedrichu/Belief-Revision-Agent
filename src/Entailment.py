import copy

from Clause import Clause
from Belief import Belief
from BeliefBase import BeliefBase


def entails(premise_base: BeliefBase, statement: str) -> bool:
    """
    Entailment (BB ⊨ φ) checking using resolution refutation - proving BB ∧ ¬φ is unsatisfiable
    :param premise_base: belief base considered as the premise
    :param statement: statement to be entailed
    :return: boolean value if the statement is entailed by the premise base
    """
    tmp_base = copy.copy(premise_base)
    # Refute the query belief - negation of the statement
    tmp_base.add_belief(Belief(f'~({statement})'))

    return tmp_base.resolution()


if __name__ == '__main__':
    # Test that the empty clause is found in the set of clauses
    assert Clause.empty_clause() in {Clause.empty_clause()}