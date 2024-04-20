from sympy.logic.boolalg import BooleanFunction, to_cnf

import BeliefBase
import Belief


class Agent:
    def __init__(self, belief_base: BeliefBase):
        self._belief_base = belief_base

    def revision(self, phi: str) -> BeliefBase:
        phi_cnf = to_cnf(phi)
        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        tmp_base = self.contract(self._belief_base, ~phi_cnf)
        return self.expand(tmp_base, phi_cnf)

    def contraction(self, phi: str) -> BeliefBase:
        contracted_base = BeliefBase.BeliefBase()
        contracted_base.beliefs = set(list(filter(lambda b: not (b == phi), self._belief_base.beliefs)))
        return contracted_base

    def expansion(self, phi: str) -> BeliefBase:
        new_belief = Belief.Belief(phi)
        self._belief_base.beliefs.add(new_belief)
        return self._belief_base
