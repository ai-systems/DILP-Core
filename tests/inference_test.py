'''File for testing inference functions (Inference.py)
'''
from src.core import Term, Atom
from src.ilp import Language_Frame, Program_Template, Rule_Template, Inference


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
    inference = Inference(program_template, language_frame)
    ground_atoms = inference.generate_ground_atoms()
    assert len(ground_atoms) == 13
