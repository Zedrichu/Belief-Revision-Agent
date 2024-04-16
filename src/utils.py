from typing import Optional

from sympy.logic.boolalg import And, Or, Not, BooleanFunction


def removeAll(item, var_set: set) -> set:
    return set([x for x in var_set if x != item])


def unique(list_seq: list) -> set:
    return set(list_seq)


def is_literal(formula: BooleanFunction):
    return isinstance(formula, Not) or not isinstance(formula, (And, Or))


def disjunction(literals: set) -> Optional[BooleanFunction]:
    if len(literals) == 0:
        return None
    elif len(literals) == 1:
        return literals.pop()
    else:
        return Or(*literals)
