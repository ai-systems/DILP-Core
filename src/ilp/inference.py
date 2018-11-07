'''Defines the inference
'''
from src.core import Atom, Clause, Term
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from itertools import product
from collections import defaultdict
from functools import reduce


class Inference():

    @staticmethod
    def f_c(clause: Clause, valuations: list, constants: list, base_map: {}):
        '''

        Arguments:
            clause {Clause} -- clause to generate f_c
            valuations {list} -- valuation list
            constants {list} -- constants
        '''
        constant_terms = [Term(False, constant) for constant in constants]
        variables = [Term(True, variable) for variable in clause.variables]
        comb = []
        for var in variables:
            temp = []
            for c in constant_terms:
                temp.append((var, c))
            comb.append(temp)
        dict_valuation = {base_map[i]:
                          valuations[i] for i in range(0, len(valuations))}
        derived_valuation = defaultdict(list)
        derived_valuation2 = defaultdict(list)
        for elm in product(*comb):
            subs = {a[0]: a[1] for a in elm}
            substituted_head = Atom(
                [subs[term] for term in clause.head.terms], clause.head.predicate)
            derived = []
            for atom in clause.body:
                substituted_body = Atom([subs[term]
                                         for term in atom.terms], atom.predicate)
                derived.append(dict_valuation[substituted_body])
            derived_valuation[substituted_head].append(
                round(reduce(lambda a, b: a * b, derived, 1), 6))
            derived_valuation2[substituted_head].append(derived)
        z_c = {}
        for atom in base_map:
            if(atom in derived_valuation):
                z_c[atom] = max(derived_valuation[atom])
            else:
                z_c[atom] = 0.0
        return z_c
