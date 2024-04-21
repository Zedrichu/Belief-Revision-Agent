from dataclasses import dataclass

from sympy.logic.boolalg import BooleanFunction, to_cnf


# @dataclass(frozen=True)
class Belief:
    cnf: BooleanFunction
    formula: str

    def __init__(self, formula: str):
        self.formula = formula
        self.cnf = to_cnf(formula)

    def __str__(self):
        return f'Belief| {str(self.formula)}'

    def __eq__(self, other):
        return self.cnf == other.cnf

    def __hash__(self):
        return hash(self.formula) ^ hash(self.cnf)
