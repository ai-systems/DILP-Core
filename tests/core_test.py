import logging
from src.core import Clause, Atom, Term
from src.ilp import Language_Frame, Rule_Template, Program_Template
from src.utils import is_intensional


logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


term1 = Term(True, 'X')
term2 = Term(False, 'USA')
term3 = Term(True, 'Y')
atom1 = Atom([term1, term2], 'PresidentOf')
atom2 = Atom([term1, term2], 'BornIn')
atom3 = Atom([term1, term3], 'BornIn')
clause = Clause(atom1, [atom2])


def core_test():
    assert term1.isVariable == True
    assert term1.name == 'X'
    assert term2.isVariable != True
    assert term2.name == 'USA'
    assert atom1.predicate == 'PresidentOf'
    assert atom1.terms == [term1, term2]
    assert atom1.arity == 2
    assert clause.head == atom1
    assert clause.body == [atom2]


def equality_test():
    term1 = Term(True, 'X_0')
    term2 = Term(True, 'X_1')
    atom1 = Atom([term1, term1], 'p')
    atom2 = Atom([term1, term2], 'p')
    head = Atom([term1, term2], 'q')
    clause1 = Clause(head, [atom1, atom2])
    clause2 = Clause(head, [atom2, atom1])
    pred_dict = {}
    pred_dict[clause1] = 1
    pred_dict[clause2] = 1
    assert clause1 == clause2
    assert len(pred_dict) == 1


def utils_test():
    assert is_intensional(atom1) == False
    assert is_intensional(atom2) == False
    assert is_intensional(atom3) == True


def language_frame_test():
    try:
        lang_frame = Language_Frame(atom1, [atom1, atom2], ['USA', 'VALUE'])
        assert False
    except ValueError as err:
        assert True

    try:
        lang_frame = Language_Frame(atom3, [atom1], ['USA'])
        assert False
    except ValueError as err:
        assert True

        lang_frame = Language_Frame(atom3, [atom3],  ['USA'])
        assert lang_frame.arity[0] == 2
        assert len(lang_frame.constants) == 1


def rule_template_test():
    rule_template = Rule_Template(1, True)
    assert rule_template.v == 1
    assert rule_template.allow_intensional == True


def program_template_test():
    rule_template = Rule_Template(1, True)
    try:
        program_template = Program_Template(
            [atom1], (rule_template, rule_template), 300)
        assert False
    except ValueError as err:
        assert True

    program_template = Program_Template(
        [atom3], (rule_template, rule_template), 300)
