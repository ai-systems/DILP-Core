'''For testing DILP
'''
from src.core import Term, Atom
from src.ilp import Language_Frame, Program_Template, Rule_Template
from src.dilp import DILP
import tensorflow as tf
tf.enable_eager_execution()


def even_numbers_test():
    B = [Atom([Term(False, '0')], 'zero')] + \
        [Atom([Term(False, str(i)), Term(False, str(i + 1))], 'succ')
         for i in range(0, 10)]

    P = [Atom([Term(False, str(i))], 'target') for i in range(0, 11, 2)]
    N = [Atom([Term(False, str(i))], 'target') for i in range(1, 11, 2)]
    term_x_0 = Term(True, 'X_0')
    term_x_1 = Term(True, 'X_1')

    p_e = [Atom([term_x_0], 'zero'), Atom([term_x_0, term_x_1], 'succ')]
    p_a = [Atom([term_x_0, term_x_1], 'pred')]
    target = Atom([term_x_0], 'target')
    constants = [str(i) for i in range(0, 11)]

    # Define rules for intensional predicates
    p_a_rule = (Rule_Template(1, False), None)
    target_rule = (Rule_Template(0, False), Rule_Template(1, True))
    rules = {p_a[0]: p_a_rule, target: target_rule}

    langage_frame = Language_Frame(target, p_e, constants)
    program_template = Program_Template(p_a, rules, 10)
    # program_template = Program_Template(p_a, rules, 300)

    dilp = DILP(langage_frame, B, P, N, program_template)

    dilp.train()


def prdecessor():
    B = [Atom([Term(False, '0')], 'zero')] + \
        [Atom([Term(False, str(i)), Term(False, str(i + 1))], 'succ')
         for i in range(0, 9)]

    P = [Atom([Term(False, str(i + 1)), Term(False, str(i))], 'target')
         for i in range(0, 9)]
    N = []
    for i in range(0, 10):
        for j in range(0, 10):
            if j != i + 1:
                N.append(
                    Atom([Term(False, str(j)), Term(False, str(i))], 'target'))
    term_x_0 = Term(True, 'X_0')
    term_x_1 = Term(True, 'X_1')

    p_e = [Atom([term_x_0], 'zero'), Atom([term_x_0, term_x_1], 'succ')]
    p_a = []

    target = Atom([term_x_0, term_x_1], 'target')
    # target_rule = (Rule_Template(0, False), Rule_Template(1, True))
    target_rule = (Rule_Template(0, False), None)
    rules = {target: target_rule}
    constants = [str(i) for i in range(0, 10)]

    langage_frame = Language_Frame(target, p_e, constants)
    program_template = Program_Template(p_a, rules, 10)
    dilp = DILP(langage_frame, B, P, N, program_template)
    dilp.train()


def less_than():
    B = [Atom([Term(False, '0')], 'zero')] + \
        [Atom([Term(False, str(i)), Term(False, str(i + 1))], 'succ')
         for i in range(0, 9)]

    P = []
    N = []
    for i in range(0, 10):
        for j in range(0, 10):
            if j <= i:
                N.append(
                    Atom([Term(False, str(j)), Term(False, str(i))], 'target'))
            else:
                P.append(
                    Atom([Term(False, str(j)), Term(False, str(i))], 'target'))

    term_x_0 = Term(True, 'X_0')
    term_x_1 = Term(True, 'X_1')

    p_e = [Atom([term_x_0], 'zero'), Atom([term_x_0, term_x_1], 'succ')]
    p_a = []

    target = Atom([term_x_0, term_x_1], 'target')
    # target_rule = (Rule_Template(0, False), Rule_Template(1, True))
    target_rule = (Rule_Template(0, False), Rule_Template(1, False))
    rules = {target: target_rule}
    constants = [str(i) for i in range(0, 10)]

    langage_frame = Language_Frame(target, p_e, constants)
    program_template = Program_Template(p_a, rules, 10)
    dilp = DILP(langage_frame, B, P, N, program_template)
    dilp.train()


less_than()
