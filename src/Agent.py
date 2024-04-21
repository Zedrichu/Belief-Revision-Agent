from sympy.logic.boolalg import BooleanFunction, to_cnf

import BeliefBase
import Belief


class Agent:
    _belief_base: BeliefBase

    def __init__(self, belief_base: BeliefBase):
        self._belief_base = belief_base

    def revision(self, phi: str) -> BeliefBase:
        phi_cnf = to_cnf(phi)
        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        self._belief_base = self.contraction(~phi_cnf)
        self._belief_base = self.expansion(phi_cnf)
        return self._belief_base

    def contraction(self, phi: str) -> BeliefBase:
        contracted_base = BeliefBase.BeliefBase()
        contracted_base.beliefs = set(list(filter(lambda b: not (b == phi), self._belief_base.beliefs)))
        return contracted_base

    def expansion(self, phi: str) -> BeliefBase:
        new_belief = Belief.Belief(phi)
        self._belief_base.add_belief(new_belief)
        return self._belief_base

    def show_belief_base(self):
        print(self._belief_base)
