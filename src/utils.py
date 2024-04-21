from typing import Optional, Set, List

from sympy.logic.boolalg import And, Or, Not, BooleanFunction


def removeAll(item, var_set: set) -> set:
    return set([x for x in var_set if x != item])


def unique(list_seq: list) -> set:
    return set(list_seq)


def is_literal(formula: BooleanFunction):
    return isinstance(formula, Not) or not isinstance(formula, (And, Or))


def disjunction_series(terms: Set[BooleanFunction]) -> Optional[BooleanFunction]:
    # Unpack positional arguments from iterable to form \/ disjunction of formulas
    return Or(*terms) if terms else None


def conjunction_series(terms: Set[BooleanFunction]) -> Optional[BooleanFunction]:
    # Unpack positional arguments from iterable to form /\ conjunction of formulas
    return And(*terms) if terms else None


def dissociate(formula: BooleanFunction, operator) -> List[BooleanFunction]:
    # Extract terms from formula based on top-level operator
    return list(formula.args) if isinstance(formula, operator) else [formula]
