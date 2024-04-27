from src.Clause import Clause


def resolution(clauses: set[Clause]):
    """
    Resolution algorithm for propositional logic in clausal form
    :param clauses: set of clauses obtained from the CNF form of premises
    :return: bool

    Pseudo-code:
    clauses = set of clauses in CNF form of KB and ¬α
    new = {}
    while True:
        for each pair of clauses Ci, Cj in clauses:
            resolvents = resolve(Ci, Cj)
            if resolvents contains the empty clause:
                return True
            new = new ∪ resolvents
        if new ⊆ clauses:
            return False
        clauses = clauses ∪ new
    """

    # Apply resolution - search for the empty clause
    while True:
        new_clauses = set()
        # Attempt to resolve each pair of clauses
        for clause1 in clauses:
            for clause2 in clauses:
                # Set of all possible resolvents if clauses are clashing
                resolvents = Clause.resolve(clause1, clause2)
                # If the empty clause is found, the clausal form is unsatisfiable
                if Clause.empty_clause() in resolvents:
                    return True
                # Add the resolvents to the new set of clauses
                new_clauses.update(resolvents)
        # No new resolvent were found - the clausal form is satisfiable (consistent)
        if new_clauses.issubset(clauses):
            return False
        # Union of the new resolvents with the set of clauses in the base
        clauses.update(new_clauses)


if __name__ == '__main__':
    # Test that the empty clause is found in the set of clauses
    assert Clause.empty_clause() in {Clause.empty_clause()}
