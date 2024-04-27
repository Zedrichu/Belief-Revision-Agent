from typing import Set
from sympy.logic.boolalg import BooleanFunction, to_cnf, Or, And

from src.Clause import Clause
from src.utils import dissociate


class Belief:
    cnf: BooleanFunction
    formula: str
    literals: set
    priority: float
    age: int

    def __init__(self, formula: str):
        self.formula = formula
        self.cnf = to_cnf(formula)
        self.literals = self.extract_literals()

    def extract_literals(self):
        literals = set()
        for clause in self.clausal_form():
            literals.update(clause.literals)
        return literals

    def clausal_form(self) -> Set[Clause]:
        """
        Convert single belief to clausal form
        :return: set of clauses derived = set of sets of literals
        """
        disjunctions = dissociate(self.cnf, And)
        clauses = set()
        for disjunction in disjunctions:
            clause = Clause(set(dissociate(disjunction, Or)))
            clauses.add(clause)
        return clauses

    def update_priority(self, priority):
        self.priority = priority

    def __str__(self):
        return f'Belief| {str(self.formula)}'

    def __eq__(self, other):
        return self.cnf == other.cnf

    def __hash__(self):
        return hash(self.cnf)
