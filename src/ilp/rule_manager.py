'''Defines the rule generating for ILP
'''
from src.core import Atom, Clause, Term
from src.utils import is_intensional


class Rule_Manger():
    def __init__(self, p_a: list,  rules: tuple, target: Atom, p_e: list):
        '''
        Arguments:
            p_a {list} -- auxiliary predicates
            arity {list} -- arity map of each predicate
            rules {tuple} -- rules tuple
            target {Atom} -- target atom to generate
            p_e {list} -- existential predicates
        '''
        self.target = target
        self.p_a = p_a
        self.rules = rules
        self.p_e = p_e

    def generate_clauses(self):
        '''Generate the clauses based on rules
        '''
        rule_matrix = []
        for rule in self.rules:
            clauses = []
            if(rule.allow_intensional):
                p = self.p_e + self.p_a + [self.target]
                p_i = self.p_a + [self.target]
                intensional_predicates = [atom.predicate for atom in p_i]
            else:
                p = self.p_e
            variables = ['X_%d' %
                         i for i in range(0, self.target.arity + rule.v)]
            target_variables = ['X_%d' %
                                i for i in range(0, self.target.arity)]

            # NOTE: Only allows 2 predicates and 2 arity maximum
            # TODO: Need for optimizing
            for i1 in range(0, len(p)):
                for v1 in variables:
                    for v2 in variables:
                        for i2 in range(i1, len(p)):
                            for v3 in variables:
                                for v4 in variables:
                                    # unsafe
                                    if not set(target_variables).issubset([v1, v2, v3, v4]):
                                        continue
                                    head = Atom(
                                        [Term(True, var) for var in target_variables], self.target.predicate)

                                    body1 = Atom(
                                        [Term(True, v1), Term(True, v2)], p[i1].predicate)
                                    body2 = Atom(
                                        [Term(True, v3), Term(True, v4)], p[i2].predicate)
                                    clause = Clause(head, [body1, body2])
                                    if head == body1 or head == body2:
                                        continue
                                    # NOTE: Based on appendix requires to have a intensional predicate
                                    if rule.allow_intensional and not (body1.predicate in intensional_predicates or body2.predicate in intensional_predicates):
                                        continue
                                    # duplicate
                                    if clause not in clauses:
                                        clauses.append(clause)
            print(clauses)
            rule_matrix.append(clauses)
        return rule_matrix
