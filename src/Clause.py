from typing import Set
from sympy.logic.boolalg import Not


class Clause:

    def __init__(self, literals: Set):
        self.literals = frozenset(literals)

    def __str__(self):
        return f'Clause| {str(self.literals)}'

    def __eq__(self, other):
        return self.literals == other.literals

    def __print__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.literals)

    def is_empty_clause(self):
        return self.literals == frozenset()

    @staticmethod
    def resolve(c1, c2):
        """
        Resolve two clauses
        :param c1: Clause
        :param c2: Clause
        :return: resolvent
        """
        clashed = False
        for i in c1.literals:
            for j in c2.literals:
                if i == Not(j) or Not(i) == j:
                    # Clashing pair of literals found in clauses
                    c1.literals = c1.literals.difference({i})
                    c2.literals = c2.literals.difference({j})
                    clashed = True
        if clashed:
            resolvent = c1.literals.union(c2.literals)
            return Clause(resolvent)
        return None
