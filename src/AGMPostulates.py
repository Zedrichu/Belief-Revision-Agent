from Agent import Agent
from BeliefBase import BeliefBase
from Resolution import resolution
import copy


class AGMPostulates:
    """
    Use the AGM postulates to test your algorithm:
        - Success postulate (success)
        - Inclusion postulate (inclusion)
        - Vacuity postulate (vacuity)
        - Consistency postulate (consistency)
        - Extensionality postulate (extensionality)
    """

    @staticmethod
    def success(belief_base: BeliefBase, phi: str):
        """
        φ ∈ B * φ
        """
        initial_belief_base = copy.copy(belief_base)

        agent = Agent(initial_belief_base)
        agent.revision(phi)
        return agent.check_entailment(phi)

    @staticmethod
    def inclusion(belief_base: BeliefBase, phi: str):
        """
        B * φ ⊆ B + φ
        """
        initial_belief_base = copy.copy(belief_base)

        agent = Agent(initial_belief_base)
        expanded_base = agent.expansion(phi)
        expanded_beliefs = expanded_base.get_beliefs()

        agent = Agent(initial_belief_base)
        revised_base = agent.revision(phi)
        revised_beliefs = revised_base.get_beliefs()

        return revised_beliefs.issubset(expanded_beliefs)

    @staticmethod
    def vacuity(belief_base: BeliefBase, phi: str):
        """
        If ¬φ ∉ B, then B * φ = B + φ
        """
        initial_belief_base = copy.copy(belief_base)

        if belief_base.entails(f'~({phi})'):
            return True

        agent = Agent(initial_belief_base)
        expanded_base = agent.expansion(phi)
        expanded_beliefs = expanded_base.get_beliefs()

        agent = Agent(initial_belief_base)
        revised_base = agent.revision(phi)
        revised_beliefs = revised_base.get_beliefs()

        return revised_beliefs == expanded_beliefs

    @staticmethod
    def consistency(belief_base: BeliefBase, phi: str):
        """
        B * φ is consistent if φ is consistent
        """
        if BeliefBase([]).entails(f'~({phi})'):
            return True

        agent = Agent(belief_base)
        revised_base = agent.revision(phi)
        return not resolution(revised_base.clausal_form())

    @staticmethod
    def extensionality(belief_base: BeliefBase, phi: str, psi: str):
        """
        If (φ ↔ φ) ∈ Cn(∅), then B * φ = B * φ
        """
        return belief_base.entails(f'{phi} >> {psi} & {psi} >> {phi}')

    # It needs to in tests, i agree.
    # But is should be checked all the time when doing revision and so
    # Like a verify

# Define like a list of properties that hold and print that after
# each revision [success, vacuity, recovery ✅❌]
