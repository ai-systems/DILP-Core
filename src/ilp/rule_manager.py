'''Defines the rule generating for ILP
'''
from src.core import Atom, Clause, Term
from src.utils import is_intensional


class Rule_Manger():
    def __init__(self, p_i: list,  rules: tuple, target: Atom, p_e: list):
        '''
        Arguments:
            p_i {list} -- intensionl predicate
            arity {list} -- arity map of each predicate
            rules {tuple} -- rules tuple
            target {Atom} -- target atom to generate
            p_e {list} -- existential predicates
        '''
        self.target = target
        self.p_i = p_i
        self.rules = rules
        self.p_e = p_e

    def generate_clauses(self):
        '''Generating clauses
        '''
        raise NotImplementedError('Code not implemented')
