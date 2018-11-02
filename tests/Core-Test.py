from src.core import Clause, Atom, Term


def core_test():
    term1 = Term(True, 'X')
    term2 = Term(False, 'USA')
    atom1 = Atom([term1, term2], 'PresidentOf')
    atom2 = Atom([term1, term2], 'BornIn')
    clause = Clause(atom1, [atom2])
    assert term1.isVariable == True
    assert term1.name == 'X'
    assert term2.isVariable != True
    assert term2.name == 'USA'
    assert atom1.name == 'PresidentOf'
    assert atom1.terms == [term1, term2]
    assert clause.head == atom1
    assert clause.body == [atom2]
