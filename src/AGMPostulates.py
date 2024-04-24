from BeliefBase import BeliefBase
from Belief import Belief


class AGMPostulates:

    @staticmethod
    def closure(self, belief_base: BeliefBase, phi: Belief):
        """
        B * φ = Cn(B * φ)
        """
        return True

    def success(self):
        """
        p ∈ B * φ
        """
        return True

    def inclusion(self):
        """
        B * φ ⊆ B + φ
        """
        return True

    def vacuity(self):
        """
        If ¬φ ∉ B, then * φ = B + φ
        """
        return True

    def consistency(self):
        """
        B * φ is consistent if φ is consistent
        """
        return True

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
