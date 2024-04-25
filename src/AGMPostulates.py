from typing import Dict, Tuple, Iterable, Optional

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

        return set(revised_beliefs).issubset(expanded_beliefs)

    @staticmethod
    def vacuity(belief_base: BeliefBase, phi: str):
        """
        If ¬φ ∉ B, then B * φ = B + φ
        """
        initial_belief_base = copy.copy(belief_base)

        if belief_base.entails(f'~({phi})'):
            return True

        expanded_beliefs = Agent(initial_belief_base).expansion(phi).get_beliefs()
        revised_beliefs = Agent(initial_belief_base).revision(phi).get_beliefs()

        return set(revised_beliefs) == set(expanded_beliefs)

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
        If (φ ↔ ψ) ∈ Cn(∅), then B * φ = B * ψ
        """
        if not BeliefBase([]).entails(f'{phi} >> {psi} & {psi} >> {phi}'):
            return True

        revision_with_phi = Agent(belief_base).revision(phi).get_beliefs()
        revision_with_psi = Agent(belief_base).revision(psi).get_beliefs()

        return set(revision_with_phi) == set(revision_with_psi)


def run_all_postulates(belief_base: BeliefBase, phi: str, psi: Optional[str] = None) -> Iterable[Tuple[str, bool]]:
    yield 'success', AGMPostulates.success(belief_base, phi)
    yield 'inclusion', AGMPostulates.inclusion(belief_base, phi)
    yield 'vacuity', AGMPostulates.vacuity(belief_base, phi)
    yield 'consistency', AGMPostulates.consistency(belief_base, phi)
    if psi is not None:
        yield 'extensionality', AGMPostulates.extensionality(belief_base, phi, psi)


def display_agm_postulates(belief_base: BeliefBase, phi: str, psi: Optional[str]):
    postulate_results = run_all_postulates(belief_base, phi, psi)
    for postulate_name, postulate_result in postulate_results:
        marker = '?' if postulate_result is None else ('✅' if postulate_result else '❌')
        print(f'{postulate_name}: {marker}')
