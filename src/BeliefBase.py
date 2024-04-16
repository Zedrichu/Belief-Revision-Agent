from typing import Set, Optional

from src.Belief import Belief


class BeliefBase:
    def __init__(self, beliefs: Optional[Set[Belief]] = None):
        self.beliefs: Set[Belief] = set()
        self.order = 0
        if beliefs:
            for belief in beliefs:
                self.add_belief(belief)

    def add_belief(self, belief: Belief):
        # Probably we should also assign how old the belief is
        self.beliefs.add(belief)
        belief.order = self.order
        self.order += 1

# currentBeliefs = [a, b, c]
# newBeliefs1 = [d, e]
# currentBeliefs = revise(currentBeliefs, newBeliefs1)
# newBeliefs2 = [...]
# currentBeliefs = revise(currentBeliefs, newBeliefs2)
