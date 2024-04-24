from itertools import combinations
from typing import Set
import numpy as np
from sympy import symbols
from sympy.logic.boolalg import to_cnf

from BeliefBase import BeliefBase
from Belief import Belief
from Entailment import entails


class Agent:
    _belief_base: BeliefBase

    def __init__(self, belief_base: BeliefBase):
        self._belief_base = belief_base

    def revision(self, phi: str) -> BeliefBase:
        """
        Revision operator for belief base BB * φ
        :param phi: the statement to be revised in string format
        :return: resulting belief base
        """
        self._belief_base.update_entrenchment()

        # # # Ignore contradictions - affect belief base consistency
        if not entails(BeliefBase([]), '~(' + phi + ')'):
            return self._belief_base

        # Ignore tautologies - automatically included in belief sets
        # Tautologies bring no inference power to the belief base
        if entails(BeliefBase([]), phi):
            return self._belief_base

        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        self._belief_base = self.contraction('~'+phi)
        self._belief_base = self.expansion(phi)
        return self._belief_base

    @staticmethod
    def selection_function(remainder_set: Set[frozenset[Belief]]) -> frozenset[Belief]:
        if len(remainder_set) == 0:
            return frozenset()

        def accumulator(remainder: frozenset[Belief]):
            return sum([b.priority for b in remainder])

        list_remainders = list(remainder_set)

        # Select the most plausible remainder
        max_entrenched = np.argmax([accumulator(rem) for rem in list_remainders])
        return list_remainders[max_entrenched]

    def contraction(self, phi: str) -> BeliefBase:
        """
        Contraction operator for belief base BB ÷ φ
        :param phi: the statement to be contracted in string format
        :return: resulting belief base
        """
        self._belief_base.update_entrenchment()

        # If phi is a tautology, return the full belief base
        if entails(BeliefBase([]), phi):
            return self._belief_base

        remainder_set = self.remainder_set(self._belief_base, phi)
        remainder = self.selection_function(remainder_set)
        contracted_base = BeliefBase(list(remainder))
        self._belief_base = contracted_base
        return self._belief_base

    def expansion(self, phi: str) -> BeliefBase:
        """
        Expansion operator for belief base BB + φ
        :param phi: the statement to be expanded in string format
        :return: resulting belief base
        """
        new_belief = Belief(phi)
        self._belief_base.update_entrenchment()

        # Verify if the belief is already implied the belief base
        if entails(self._belief_base, phi):
            return self._belief_base

        # Verify if the belief is already explicit in the belief base
        if new_belief not in self._belief_base.get_beliefs():
            self._belief_base.add_belief(new_belief)

        return self._belief_base

    @staticmethod
    def remainder_set(bbase: BeliefBase, phi: str) -> Set[frozenset[Belief]]:
        remainder = set()
        maximal_inclusion = False
        beliefs = bbase.get_beliefs()
        for depth in range(len(beliefs), 0, -1):
            for subset in combinations(beliefs, depth):
                belief_base = BeliefBase(list(subset))

                if not entails(belief_base, phi):
                    remainder.add(frozenset(subset))
                    maximal_inclusion = True

            if maximal_inclusion:
                break

        return remainder

    def check_entailment(self, query: str):
        """
        Verify consistency of a statement with the belief base (entailment)
        :param query: the statement to be checked in string format
        :return: boolean - entailed or not
        """
        return entails(self._belief_base, query)

    def check_consistent(self, query: str):
        """
        Verify consistency of a statement with the belief base (refutation entailment)
        :param query: the statement to be checked in string
        :return: boolean - consistent or inconsistent
        """
        return not entails(self._belief_base, '~'+query)

    def show_belief_base(self):
        print(self._belief_base)


if __name__ == '__main__':
    # beliefs = [Belief('p'), Belief('p | q'), Belief('p & q'), Belief('(p >> q) & (q >> p)')]
    # base = BeliefBase(beliefs)
    # print(base)
    # god = Agent(base)
    # rem = Agent.remainder_set(base, 'p')
    # for r in rem:
    #     for b in r:
    #         print(b)
    # base.update_entrenchment()
    # # selected = Agent.selection_function(rem)
    # print(god.contraction('p'))
    beliefs = [Belief('p'), Belief('q'), Belief('p >> q')]
    base = BeliefBase(beliefs)
    god = Agent(base)
    print(god.revision('~q'))
    pass

