from sympy.logic.boolalg import BooleanFunction, to_cnf

import BeliefBase
import Belief


class Agent:
    def __init__(self, belief_base: BeliefBase):
        self.belief_base = belief_base

    def revision(self, belief_base: BeliefBase, phi: BooleanFunction) -> BeliefBase:
        phi_cnf = to_cnf(phi)
        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        tmp_base = self.contract(belief_base, ~phi_cnf)
        return self.expand(tmp_base, phi_cnf)

    def contract(self, belief_base: BeliefBase, phi: str) -> BeliefBase:
        contracted_base = BeliefBase.BeliefBase()
        contracted_base.beliefs = set(list(filter(lambda b: not (b == phi), belief_base.beliefs)))
        return contracted_base

    def expand(self, belief_base: BeliefBase, phi: str) -> BeliefBase:
        new_belief = Belief.Belief(phi)
        belief_base.beliefs.add(new_belief)
        return belief_base
