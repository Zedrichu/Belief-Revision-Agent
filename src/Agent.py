from sympy import symbols
from sympy.logic.boolalg import BooleanFunction, to_cnf

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
        phi_cnf = to_cnf(phi)
        # Apply Levi's identity for the revision operator to the belief base (B * φ = (B ÷ ¬φ) + φ)
        self._belief_base = self.contraction(~phi_cnf)
        self._belief_base = self.expansion(phi_cnf)
        return self._belief_base

    def contraction(self, phi: str) -> BeliefBase:
        """
        Contraction operator for belief base BB ÷ φ
        :param phi: the statement to be contracted in string format
        :return: resulting belief base
        """
        neg_cnf = to_cnf(phi)
        contracted_base = BeliefBase()
        print(neg_cnf)

        # #for belief in self._belief_base.get_beliefs():
        # #        if belief == neg_cnf
        #
        # contracted_base.beliefs = set(list(filter(lambda b: not (b == phi), self._belief_base.beliefs)))
        # return contracted_base

    def expansion(self, phi: str) -> BeliefBase:
        """
        Expansion operator for belief base BB + φ
        :param phi: the statement to be expanded in string format
        :return: resulting belief base
        """
        new_belief = Belief(phi)

        # Verify if the belief is already implied the belief base
        if entails(self._belief_base, phi):
            return self._belief_base

        # Verify if the belief is already explicit in the belief base
        if new_belief not in self._belief_base.get_beliefs():
            self._belief_base.add_belief(new_belief)

        return self._belief_base

    def check(self, query: str):
        """
        Verify consistency of a statement with the belief base (entailment)
        :param query: the statement to be checked in string format
        :return: resulting the belief state
        """
        return entails(self._belief_base, query)

    def show_belief_base(self):
        print(self._belief_base)


if __name__ == '__main__':
    # Create the initial belief base in a Agent
    p, q, r = symbols('p, q, r')
    beliefs = [Belief(p), Belief(q), Belief(r)]
    belief_base = BeliefBase(beliefs)
    agent = Agent(belief_base)

    # Do new learning
    new_knowledge = "~(q | r)"
    new_belief_base = agent.revision(new_knowledge)

    #beliefs = [Belief('A >> B'), Belief('A')]
    #base = BeliefBase(beliefs)
    #agent = Agent(base)
    #agent.show_belief_base()
    #agent.expansion('B')
    #agent.show_belief_base()
    pass

