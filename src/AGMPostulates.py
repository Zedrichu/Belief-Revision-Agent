from BeliefBase import BeliefBase
from Belief import Belief


class AGMPostulates:

    @staticmethod
    def closure(belief_base: BeliefBase, phi: Belief):
        """
        B * φ = Cn(B * φ)
        """
        return True

    @staticmethod
    def success(belief_base: BeliefBase, phi: Belief):
        """
        p ∈ B * φ
        """
        return True

    @staticmethod
    def inclusion(belief_base: BeliefBase, phi: Belief):
        """
        B * φ ⊆ B + φ
        """
        belief_base.add_belief(phi)
        return phi in belief_base.get_beliefs()

    @staticmethod
    def vacuity(belief_base: BeliefBase, phi: Belief):
        """
        If ¬φ ∉ B, then * φ = B + φ
        """
        return True

    @staticmethod
    def consistency(self):
        """
        B * φ is consistent if φ is consistent
        """
        return True

    @staticmethod
    def extensionality(self):
        """
        If (φ ↔ φ) ∈ Cn(∅), then B * φ = B * φ
        """
        return True

    def super_expansion(self):
        """
        B * (p & q) ⊆ (K * p) + q
        """
        return True

    def sub_expansion(self):
        """
        If ¬q ∉ Cn(K * p) then (K * p) + q ⊆ K * (p & q)
        """
        pass

    # It needs to in tests, i agree.
    # But is should be checked all the time when doing revision and so
    # Like a verify

# Define like a list of properties that hold and print that after
# each revision [success, vacuity, recovery ✅❌]
