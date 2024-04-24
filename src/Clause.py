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

    @classmethod
    def empty_clause(cls):
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
        # Iterate over literals to find clashing pairs
        for i in c1.literals:
            if Not(i) in c2.literals:
                # Clashing pair of literals found in clauses
                tmp1 = c1.literals.difference({i})
                tmp2 = c2.literals.difference({Not(i)})
                resolved_clause = Clause(tmp1.union(tmp2))
                if resolved_clause == Clause.empty_clause():
                    return {resolved_clause}
                resolvents.add(Clause(tmp1.union(tmp2)))
                # print(f'Found clashing literals: {i} and {Not(i)}')

        # Remove trivial clauses from resolvents
        # ex. l and ~l found in the same clause
        tmp = resolvents.copy()
        for resolvent in tmp:
            for literal in resolvent.literals:
                if Not(literal) in resolvent.literals:
                    resolvents.remove(resolvent)
                    break

        return resolvents
