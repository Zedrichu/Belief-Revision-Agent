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

    @staticmethod
    def empty_clause():
        return Clause(set())

    @staticmethod
    def resolve(c1, c2) -> Set:
        """
        Resolve two clauses
        :param c1: Clause
        :param c2: Clause
        :return: resolvent set of clauses
        """
        resolvents = set()
        for i in c1.literals:
            # Otherwise if it doesn't work reliably
            # for j in c2.literals:
            #     if i == Not(j) or Not(i) == j:
            if Not(i) in c2.literals:
                # print(f'Found clashing literals: {i} and {Not(i)}')
                # Clashing pair of literals found in clauses
                tmp1 = c1.literals.difference({i})
                tmp2 = c2.literals.difference({Not(i)})
                resolvents.add(Clause(tmp1.union(tmp2)))

        # Remove trivial clauses from resolvents
        # ex. l and ~l found in the same clause
        tmp = resolvents.copy()
        for resolvent in tmp:
            for literal in resolvent.literals:
                if Not(literal) in resolvent.literals:
                    resolvents.remove(resolvent)
                    break

        return resolvents
