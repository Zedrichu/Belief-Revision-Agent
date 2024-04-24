from Clause import Clause
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
        if empty_base.resolution():
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

    def resolution(self):
        """
        Resolution refutation algorithm for propositional logic
        :return: bool

        Pseudo-code:
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

        # Split the base into conjunctions of clauses - set of clauses
        clauses = self.clausal_form()

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

    def __str__(self):
        return (f'BeliefBase|\n\t'
                f'{'\n\t'.join(map(str, self._beliefs))}')

    def __copy__(self):
        return BeliefBase([belief for belief in self._beliefs])
