% resolution.pl

%
% Propositional resolution
%

:- ensure_loaded(logic).

resolution(XFml) :-
  NegFml = ~XFml,
  write(NegFml), nl,
  to_internal(NegFml,Fml),
  cnf(Fml,Cnf),
  to_external(Cnf,XCnf),
  write(XCnf), nl,
  cnf_to_clausal(Cnf,Cls),
  write(Cls), nl,
  resolve(Cls), !.

resolve(S) :- member([],S), !.
resolve(S) :-
  member(C1,S),
  member(C2,S),
  clashing(C1,L1,C2,L2),
  delete(C1,L1,C1P),
  delete(C2,L2,C2P),
  union(C1P,C2P,C),
  \+ clashing(C,_,C,_),
  \+ member(C,S),
  write([C|S]), nl,
  resolve([C|S]).

clashing(C1,L,C2,neg L) :-
  member(L,C1), member(neg L,C2), !.
clashing(C1,neg L,C2,L) :-
  member(neg L,C1), member(L,C2), !.

%
% cnf(A,B)
%   B is A in conjunctive normal form.
%
cnf(A,A3) :-
  eliminate(A,A1),
  demorgan(A1,A2),
  distribute(A2,A3).

%
% eliminate(A,B)
%   B is A without eqv, dif and imp.
%
eliminate(A eqv B,C) :- !,
  C = (A1 con B1) dis ((neg A1) con (neg B1)),
  eliminate(A,A1), eliminate(B,B1).
eliminate(A dif B,C) :- !,
  C = (A1 con (neg B1)) dis ((neg A1) con B1),
  eliminate(A,A1), eliminate(B,B1).
eliminate(A imp B,C) :- !,
  C = (neg A1) dis B1,
  eliminate(A,A1), eliminate(B,B1).
eliminate(A dis B,A1 dis B1) :- !,
  eliminate(A,A1), eliminate(B,B1).
eliminate(A con B,A1 con B1) :- !,
  eliminate(A,A1), eliminate(B,B1).
eliminate(neg A,neg A1) :- !,
  eliminate(A,A1).
eliminate(A,A).

%
% demorgan(A,B)
%   B is A with negations pushed inwards and reducing double negations.
%
demorgan(neg (A con B),C) :- !,
  C = A1 dis B1,
  demorgan(neg A,A1), demorgan(neg B,B1).
demorgan(neg (A dis B),C) :- !,
  C = A1 con B1,
  demorgan(neg A,A1), demorgan(neg B,B1).
demorgan(A con B,A1 con B1) :- !,
  demorgan(A,A1), demorgan(B,B1).
demorgan(A dis B,A1 dis B1) :- !,
  demorgan(A,A1), demorgan(B,B1).
demorgan((neg (neg A)),A1) :- !,
  demorgan(A,A1).
demorgan(A,A).

%
% distribute(A,B)
%   B is A with disjuntion distributed over conjunction.
%
distribute(A con B,A1 con B1) :- !,
  distribute(A,A1),
  distribute(B,B1).
distribute(A dis B,AB) :- !,
  distribute(A,A1),
  distribute(B,B1),
  distribute(A1,B1,AB).
distribute(A,A).

%
% Take two formulas in CNF and return the disjunction of these formulas in CNF.
%
distribute(A con B,C,D) :- !,
  D = D1 con D2,
  distribute(A,C,D1),
  distribute(B,C,D2).
distribute(C,A con B,D) :- !,
  D = D1 con D2,
  distribute(C,A,D1),
  distribute(C,B,D2).
distribute(A,B,A dis B).

%
% cnf_to_clausal(A,S)
%   A is a CNF formula, S is the formula in clausal notation.
%
cnf_to_clausal(A1 con A2,S) :- !,
  cnf_to_clausal(A1,S1),
  cnf_to_clausal(A2,S2),
  union(S1,S2,S).
cnf_to_clausal(A,S) :-
  disjunction_to_clause(A,C),
  ( clashing(C,_,C,_) ->
    S = []
  ;
    S = [C]
  ).

%
% Only disjunctions remain.
%
disjunction_to_clause(A1 dis A2,S) :- !,
  disjunction_to_clause(A1,S1),
  disjunction_to_clause(A2,S2),
  union(S1,S2,S).
disjunction_to_clause(A,[A]).