from src.core import Clause, Atom, Term
from src.ilp import Rule_Template, Rule_Manger


def rule_test1():
    rule_template_1 = Rule_Template(0, False)
    rule_template_2 = Rule_Template(1, True)
    target = Atom([Term(True, 'X_0'), Term(True, 'X_1')], 'q')
    p_e = [Atom([Term(True, 'X_0'), Term(True, 'X_1')], 'p')]
    rule_manager = Rule_Manger(
        [], (rule_template_1, rule_template_2), target, p_e)
    rule_matrix = rule_manager.generate_clauses()
    assert len(rule_matrix[0]) == 8
    print(len(rule_matrix[1]))
    assert len(rule_matrix[1]) == 58
