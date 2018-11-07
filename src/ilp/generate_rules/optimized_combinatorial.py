'''Optimized combinatorial class
'''
import logging

from src.ilp import Rule_Manger
from src.core import Atom, Term, Clause

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Optimized_Combinatorial_Generator(Rule_Manger):

    def generate_clauses(self):
        '''Generate all clauses with some level of optimization
        '''
        rule_matrix = []
        for rule in self.rules:
            # logger.info('Generating clauses')
            if rule == None:
                rule_matrix.append([None])
                continue
            clauses = []
            if(rule.allow_intensional):
                p = list(set(self.p_e + self.p_i + [self.target]))
                p_i = list(set(self.p_i))
                intensional_predicates = [atom.predicate for atom in p_i]
            else:
                p = list(set(self.p_e))
            variables = ['X_%d' %
                         i for i in range(0, self.target.arity + rule.v)]
            target_variables = ['X_%d' %
                                i for i in range(0, self.target.arity)]

            # Generate the body list
            body_list = []
            head = Atom(
                [Term(True, var) for var in target_variables], self.target.predicate)
            for var1 in variables:
                for var2 in variables:
                    term1 = Term(True, var1)
                    term2 = Term(True, var2)
                    body_list.append([term1, term2])
            # Generate the list
            added_pred = {}
            for ind1 in range(0, len(p)):
                pred1 = p[ind1]
                for b1 in body_list:
                    for ind2 in range(ind1, len(p)):
                        pred2 = p[ind2]
                        for b2 in body_list:
                            body1 = Atom([b1[index]
                                          for index in range(0, pred1.arity)], pred1.predicate)
                            body2 = Atom([b2[index]
                                          for index in range(0, pred2.arity)], pred2.predicate)

                            clause = Clause(head, [body1, body2])
                            # logger.info(clause)
                            # All variables in head should be in the body
                            if not set(target_variables).issubset([v.name for v in b1] + [v.name for v in b2]):
                                continue
                            elif head == body1 or head == body2:  # No Circular
                                continue
                            # NOTE: Based on appendix requires to have a intensional predicate
                            elif rule.allow_intensional and not (body1.predicate in intensional_predicates or body2.predicate in intensional_predicates):
                                continue
                            elif clause in added_pred:
                                continue
                            else:
                                added_pred[clause] = 1
                                clauses.append(clause)
            rule_matrix.append(clauses)
            # logger.info('Clauses Generated')
        return rule_matrix
