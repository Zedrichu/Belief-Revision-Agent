from sympy import symbols

from Clause import Clause
from utils import *
from typing import List, Optional
from src.Belief import Belief


class BeliefBase:
    _beliefs: List[Belief]
    order: int

    def __init__(self, beliefs: Optional[List[Belief]] = None):
        self._beliefs = []
        self.order = 0
        if beliefs:
            for belief in beliefs:
                self.add_belief(belief)

    def add_belief(self, belief: Belief):
        # Probably we should also assign how old the belief is
        self._beliefs.append(belief)
        belief.order = self.order
        self.order += 1

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

    def __str__(self):
        return (f'BeliefBase|\n\t'
                f'{'\n\t'.join(map(str, self._beliefs))}')

    def __copy__(self):
        return BeliefBase([belief for belief in self._beliefs])
