import copy

from Clause import Clause
from Resolution import resolution
from utils import *
from typing import List, Optional
from src.Belief import Belief


class BeliefBase:
    _beliefs: List[Belief]

    def __init__(self, beliefs: Optional[List[Belief]] = None):
        self._beliefs = []
        if beliefs:
            for belief in beliefs:
                self.add_belief(belief)

    def get_beliefs(self):
        return self._beliefs

    def add_belief(self, belief: Belief):
        self._beliefs.append(belief)

    def update_entrenchment(self):
        for belief in self._beliefs:
            epistemic_value = self.epistemic(belief)
            belief.update_priority(epistemic_value)

    @staticmethod
    def epistemic(belief: Belief) -> float:
        # Tautologies are most entrenched
        empty_base = BeliefBase([Belief('~'+belief.formula)])
        clauses = empty_base.clausal_form()
        if resolution(clauses):
            return 1

        num_literals = len(belief.literals)
        return 1 / (num_literals + 1)

    def remove_belief(self, belief: Belief):
        self._beliefs.remove(belief)

    def remove_indexed_belief(self, index: int):
        self._beliefs.pop(index)

    def clausal_form(self) -> Set[Clause]:
        """
        Convert belief base to clausal form
        :return: set of clauses = set of sets of literals
        """
        cnf_belief_base = set([belief.cnf for belief in self._beliefs])
        # CNF of overall conjunction of beliefs
        full_belief = conjunction_series(cnf_belief_base)

        clausal_form = set()
        disjunctions = dissociate(full_belief, And)
        for disjunction in disjunctions:
            clause = Clause(set(dissociate(disjunction, Or)))
            clausal_form.add(clause)
        return clausal_form

    def entails(self, statement: str) -> bool:
        """
        Entailment (BB ⊨ φ) checking by resolution refutation proof - proving BB ∧ ¬φ is unsatisfiable
        :param statement: statement to be entailed
        :return: boolean value if the statement is entailed by the premise base
        """
        tmp_base = copy.copy(self)
        # Refute the query belief - negation of the statement
        tmp_base.add_belief(Belief(f'~({statement})'))

        # Transform assumption to clausal form & apply resolution
        return resolution(tmp_base.clausal_form())

    def __str__(self):
        return (f'BeliefBase|\n\t'
                f'{'\n\t'.join(map(str, self._beliefs))}')

    def __copy__(self):
        return BeliefBase([belief for belief in self._beliefs])
