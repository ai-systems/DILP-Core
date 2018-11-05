'''File for testing inference functions (Inference.py)
'''
from src.core import Term, Atom, Clause
from src.ilp import Language_Frame, Program_Template, Rule_Template, Inference, ILP

term1 = Term(True, 'X_0')
term2 = Term(True, 'X_1')
target = Atom([term1, term2], 'r')
p_e = [Atom([term1, term2], 'p')]
p_a = [Atom([term1, term2], 'q')]

rule_template_1 = Rule_Template(0, False)
rule_template_2 = Rule_Template(1, True)

language_frame = Language_Frame(target, p_e, set(['a', 'b']))
program_template = Program_Template(
    p_a, (rule_template_1, rule_template_2), 300)

term_a = Term(False, 'a')
term_b = Term(False, 'b')
# Background facts: p(a,a) p(a,b)
background = [Atom([term_a, term_a], 'p'), Atom([term_a, term_b], 'p')]
# Positive: p(b,a)
positive = [Atom([term_b, term_a], 'p')]
# Negative: p(b,b)
negative = [Atom([term_b, term_b], 'p')]
ilp = ILP(language_frame, background, positive, negative, program_template)
initial_valuation = ilp.convert()


def f_c_test():
    '''Testing f_c function
    '''
    term_x = Term(True, 'X_0')
    term_y = Term(True, 'X_1')
    term_z = Term(True, 'X_2')
    r = Atom([term_x, term_y], 'r')
    p = Atom([term_x, term_z], 'p')
    q = Atom([term_z, term_y], 'q')
    clause = Clause(r, [p, q])

    # Example from the book
    example_val = {Atom([term_a, term_a], 'p'): 1.0,
                   Atom([term_a, term_b], 'p'): 0.9,
                   Atom([term_a, term_a], 'q'): 0.1,
                   Atom([term_b, term_a], 'q'): 0.2,
                   Atom([term_b, term_b], 'q'): 0.8,
                   }
    modified_val = []
    for val in initial_valuation:
        if val[0] in example_val:
            modified_val.append((val[0], example_val[val[0]]))
        else:
            modified_val.append((val[0], 0))

    f_c = Inference.f_c(clause, modified_val, ['a', 'b'])
    assert f_c[Atom([term_a, term_b], 'r')] == 0.72
    assert f_c[Atom([term_a, term_a], 'r')] == 0.18
    for key in f_c:
        if key == Atom([term_a, term_b], 'r') or key == Atom([term_a, term_a], 'r'):
            continue
        else:
            assert f_c[key] == 0.0


def f_c_test2():
    '''Testing f_c function
    '''
    term1 = Term(True, 'X_0')
    term2 = Term(True, 'X_1')
    target = Atom([term1], 'r')
    p_e = [Atom([term1, term2], 'p')]
    p_a = [Atom([term1, term2], 'q')]

    rule_template_1 = Rule_Template(0, False)
    rule_template_2 = Rule_Template(1, True)

    language_frame = Language_Frame(target, p_e, set(['a', 'b']))
    program_template = Program_Template(
        p_a, (rule_template_1, rule_template_2), 300)

    term_a = Term(False, 'a')
    term_b = Term(False, 'b')
    # Background facts: p(a,a) p(a,b)
    background = [Atom([term_a, term_a], 'p'), Atom([term_a, term_b], 'p')]
    # Positive: p(b,a)
    positive = [Atom([term_b, term_a], 'p')]
    # Negative: p(b,b)
    negative = [Atom([term_b, term_b], 'p')]
    ilp = ILP(language_frame, background, positive, negative, program_template)
    initial_valuation = ilp.convert()

    term_x = Term(True, 'X_0')
    term_y = Term(True, 'X_1')
    term_z = Term(True, 'X_2')
    r = Atom([term_x], 'r')
    p = Atom([term_x, term_z], 'p')
    q = Atom([term_z, term_y], 'q')
    clause = Clause(r, [p, q])

    # Example from the book
    example_val = {Atom([term_a, term_a], 'p'): 1.0,
                   Atom([term_a, term_b], 'p'): 0.9,
                   Atom([term_a, term_a], 'q'): 0.1,
                   Atom([term_b, term_a], 'q'): 0.2,
                   Atom([term_b, term_b], 'q'): 0.8,
                   }
    modified_val = []
    for val in initial_valuation:
        if val[0] in example_val:
            modified_val.append((val[0], example_val[val[0]]))
        else:
            modified_val.append((val[0], 0))

    f_c = Inference.f_c(clause, modified_val, ['a', 'b'])
    print(f_c)
    assert f_c[Atom([term_a], 'r')] == 0.72
    for key in f_c:
        if key == Atom([term_a], 'r'):
            continue
        else:
            assert f_c[key] == 0.0


def f_c_test3():
    '''Testing f_c function
    '''
    term1 = Term(True, 'X_0')
    term2 = Term(True, 'X_1')
    target = Atom([], 'r')
    p_e = [Atom([term1, term2], 'p')]
    p_a = [Atom([term1, term2], 'q')]

    rule_template_1 = Rule_Template(0, False)
    rule_template_2 = Rule_Template(1, True)

    language_frame = Language_Frame(target, p_e, set(['a', 'b']))
    program_template = Program_Template(
        p_a, (rule_template_1, rule_template_2), 300)

    term_a = Term(False, 'a')
    term_b = Term(False, 'b')
    # Background facts: p(a,a) p(a,b)
    background = [Atom([term_a, term_a], 'p'), Atom([term_a, term_b], 'p')]
    # Positive: p(b,a)
    positive = [Atom([term_b, term_a], 'p')]
    # Negative: p(b,b)
    negative = [Atom([term_b, term_b], 'p')]
    ilp = ILP(language_frame, background, positive, negative, program_template)
    initial_valuation = ilp.convert()

    term_x = Term(True, 'X_0')
    term_y = Term(True, 'X_1')
    term_z = Term(True, 'X_2')
    r = Atom([], 'r')
    p = Atom([term_x, term_z], 'p')
    q = Atom([term_z, term_y], 'q')
    clause = Clause(r, [p, q])

    # Example from the book
    example_val = {Atom([term_a, term_a], 'p'): 1.0,
                   Atom([term_a, term_b], 'p'): 0.9,
                   Atom([term_a, term_a], 'q'): 0.1,
                   Atom([term_b, term_a], 'q'): 0.2,
                   Atom([term_b, term_b], 'q'): 0.8,
                   }
    modified_val = []
    for val in initial_valuation:
        if val[0] in example_val:
            modified_val.append((val[0], example_val[val[0]]))
        else:
            modified_val.append((val[0], 0))

    f_c = Inference.f_c(clause, modified_val, ['a', 'b'])
    print(f_c)
    assert f_c[Atom([], 'r')] == 0.72
    for key in f_c:
        if key == Atom([], 'r'):
            continue
        else:
            assert f_c[key] == 0.0
