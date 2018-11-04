'''Test ilp/__init__.py
'''

from src.core import Term, Atom
from src.ilp import Language_Frame, Program_Template, Rule_Template, Inference, ILP


# def generate_ground_atoms_test():
#     term1 = Term(True, 'X_0')
#     term2 = Term(True, 'X_1')
#     target = Atom([term1, term2], 'r')
#     p_e = [Atom([term1, term2], 'p')]
#     p_a = [Atom([term1, term2], 'q')]

#     rule_template_1 = Rule_Template(0, False)
#     rule_template_2 = Rule_Template(1, True)

#     language_frame = Language_Frame(target, p_e, set(['a', 'b']))
#     program_template = Program_Template(
#         p_a, (rule_template_1, rule_template_2), 300)
#     ground_atoms =inference.generate_ground_atoms()
#     assert len(ground_atoms) == 13


def generate_ground_atoms_test():
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
    for valuation in initial_valuation:
        if valuation[0] in background:
            assert valuation[1] == 1
        else:
            assert valuation[1] == 0
