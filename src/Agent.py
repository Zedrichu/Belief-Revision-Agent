import copy
from itertools import combinations
from typing import Set, List

from src.BeliefBase import BeliefBase
from src.Belief import Belief


class Agent:
    _belief_base: BeliefBase
    HYPER = 0.7

    def __init__(self, belief_base: BeliefBase):
        self._belief_base = copy.copy(belief_base)

    def revision(self, phi: str) -> BeliefBase:
        """
        Revision operator for belief base BB * φ
        :param phi: the statement to be revised in string format
        :return: resulting belief base
        """
        self._belief_base.update_entrenchment()

        # # # Ignore contradictions - affect belief base consistency
        if BeliefBase([]).entails(f'~({phi})'):
            return self._belief_base

        # Ignore tautologies - automatically included in belief sets
        # Tautologies bring no inference power to the belief base
        if BeliefBase([]).entails(phi):
            return self._belief_base

        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        self._belief_base = self.contraction(f'~({phi})')
        self._belief_base = self.expansion(phi)
        return self._belief_base

    def contraction(self, phi: str) -> BeliefBase:
        """
        Contraction operator for belief base BB ÷ φ
        :param phi: the statement to be contracted in string format
        :return: resulting belief base
        """
        self._belief_base.update_entrenchment()

        # If phi is a tautology, return the full belief base
        if BeliefBase([]).entails(phi):
            return self._belief_base

        # Compute the remainder set for the contraction BB ⊥ φ
        remainder_set = self.remainder_set(self._belief_base, phi)
        # Apply the selection function to the remainder set
        entrenched_remainders = self.selection_function(remainder_set)

        # Perform partial meet (kernel) contraction on selected remainders
        kernel = set()
        for rem in entrenched_remainders:
            kernel = kernel.intersection(rem)

        # Default to the most plausible remainder (maxi-choice contraction) if partial meet is empty
        if len(kernel) == 0 and len(entrenched_remainders) > 0:
            kernel = entrenched_remainders[0]

        contracted_base = BeliefBase(list(kernel))
        self._belief_base = contracted_base
        return self._belief_base

    def entrenched_contraction(self, phi: str) -> BeliefBase:
        """
        Entrenchment-based contraction operator for belief base BB ÷ φ
        q ∈ K ÷ p iff q ∈ K and either p < (p ∨ q) or p ∈ Cn(∅)
        :param phi: the statement to be contracted in string format
        :return: resulting belief base
        """
        self._belief_base.update_entrenchment()
        contracted = []

        for belief in self._belief_base.get_beliefs():
            tautology = BeliefBase([]).entails(phi)

            contractor = Belief(phi)
            contractor.update_priority(self._belief_base.epistemic(contractor))

            disjunction = Belief(f'{phi} | ({belief.formula})')
            disjunction.update_priority(self._belief_base.epistemic(disjunction))

            if tautology or contractor.priority < disjunction.priority:
                contracted.append(belief)

        self._belief_base = BeliefBase(contracted)
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
        if self._belief_base.entails(phi):
            return self._belief_base

        # Verify if the belief is already explicit in the belief base
        if new_belief not in self._belief_base.get_beliefs():
            self._belief_base.add_belief(new_belief)

        return self._belief_base

    @staticmethod
    def selection_function(remainder_set: Set[frozenset[Belief]]) -> List[frozenset[Belief]]:
        """
        Selection function γ utility used to perform the partial meet contraction based on entrenchment
        :param remainder_set: the set of valid remainders to be selected from
        :return: list of selected most entrenched remainders
        """
        if len(remainder_set) == 0:
            return [frozenset()]

        def accumulator(remainder: frozenset[Belief]):
            return sum([b.priority for b in remainder])

        list_remainders = list(remainder_set)

        # Sort the remainders by entrenchment in decreasing order (most entrenched first)
        list_remainders.sort(key=lambda x: accumulator(x), reverse=True)
        pivot = accumulator(list_remainders[0]) * Agent.HYPER # Maxi-choice threshold
        return [r for r in list_remainders if accumulator(r) >= pivot]

        # # Select the most plausible remainder
        # max_entrenched = np.argmax([accumulator(rem) for rem in list_remainders])
        # return [list_remainders[max_entrenched]]

    @staticmethod
    def remainder_set(bbase: BeliefBase, phi: str) -> Set[frozenset[Belief]]:
        """
        Compute the remainder set for the contraction BB ⊥ φ
        :param bbase: the belief base to be contracted
        :param phi: the statement to be contracted
        :return: set of valid remainders C ⊆ BB, C ⊭ φ - set of sets of beliefs
        """
        remainder = set()
        maximal_inclusion = False
        beliefs = bbase.get_beliefs()
        for depth in range(len(beliefs), 0, -1):
            for subset in combinations(beliefs, depth):
                belief_base = BeliefBase(list(subset))

                if not belief_base.entails(phi):
                    remainder.add(frozenset(subset))
                    maximal_inclusion = True

            if maximal_inclusion:
                break

        return remainder

    def check_entailment(self, query: str):
        """
        Verify entailment of a statement from the belief base
        :param query: the statement to be checked in string format
        :return: boolean - entailed or not
        """
        return self._belief_base.entails(query)

    def check_consistent(self, query: str):
        """
        Verify consistency of a statement with the belief base (refutation entailment)
        :param query: the statement to be checked in string
        :return: boolean - consistent or inconsistent
        """

        return not self._belief_base.entails(f'~({query})')

    def get_belief_base(self) -> BeliefBase:
        return copy.copy(self._belief_base)



if __name__ == '__main__':
    beliefs = [Belief('p'), Belief('p | q'), Belief('p & q'), Belief('(p >> q) & (q >> p)')]
    base = BeliefBase(beliefs)
    print(base)
    god = Agent(base)
    rem = Agent.remainder_set(base, 'p')
    for r in rem:
        for b in r:
            print(b)
    base.update_entrenchment()
    # selected = Agent.selection_function(rem)
    print(god.contraction('p'))
    pass
