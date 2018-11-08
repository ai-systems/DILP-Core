'''Defines the inference
'''
from src.core import Atom, Clause, Term
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from itertools import product
from collections import defaultdict
from functools import reduce
from collections import OrderedDict
import numpy as np


class Inference():

    @staticmethod
    def f_c(clause: Clause, valuations, dict_valuation: dict, constants: list):
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
        # dict_valuation = {valuations[i][0]:
            #   valuations[i][1] for i in range(0, len(valuations))}
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
                derived.append(valuations[dict_valuation[substituted_body]])
            derived_valuation[substituted_head].append(
                reduce(lambda a, b: a * b, derived, 1))
            derived_valuation2[substituted_head].append(derived)

        z_c = np.zeros(valuations.shape[0], dtype=np.float32)
        for atom in dict_valuation:
            if(atom in derived_valuation):
                z_c[dict_valuation[atom]] = max(derived_valuation[atom])
            else:
                z_c[dict_valuation[atom]] = 0
        return z_c

    @staticmethod
    def x_c(clause: Clause, dict_valuation: dict, constants: list):
        '''

        Arguments:
            clause {Clause} -- clause to generate f_c
            valuations {list} -- valuation list
            constants {list} -- constants
        '''
        if clause == None:
            return np.zeros((len(dict_valuation), 1, 2), dtype=int)
        constant_terms = [Term(False, constant) for constant in constants]
        head_variables = clause.head.variables
        variables = [Term(True, variable) for variable in clause.variables]
        existential_variable = len(variables) - len(head_variables)
        comb = []
        for var in variables:
            temp = []
            for c in constant_terms:
                temp.append((var, c))
            comb.append(temp)
        w = np.power(
            len(constants), existential_variable)
        x_c = np.zeros((len(dict_valuation), w, 2), dtype=int)
        derived_valuation = defaultdict(list)
        for elm in product(*comb):
            subs = {a[0]: a[1] for a in elm}
            substituted_head = Atom(
                [subs[term] for term in clause.head.terms], clause.head.predicate)
            derived = []
            for atom in clause.body:
                substituted_body = Atom([subs[term]
                                         for term in atom.terms], atom.predicate)
                derived.append(int(dict_valuation[substituted_body]))
            derived_valuation[substituted_head].append(derived)
        for atom in derived_valuation:
            for i in range(0, len(derived_valuation[atom])):
                x_c[dict_valuation[atom], i, 0] = derived_valuation[atom][i][0]
                x_c[dict_valuation[atom], i, 1] = derived_valuation[atom][i][1]
        return x_c
