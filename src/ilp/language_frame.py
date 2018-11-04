"""Defines the language frame for ILP
"""
from src.core import Atom, Term
from src.utils import is_intensional, INTENSIONAL_REQUIRED_MESSAGE


class Language_Frame():

    def __init__(self, target: Atom, p_e: list,  constants: set):
        '''

        Arguments:
            target {Atom} -- Target predicate, the intensional predicate we are trying to learn
            p_e {list} -- Set of extensional predicates
            constants {set} -- Set of constants
        '''
        arity = [
        ]  # Map p_e U {target} -> N specifyig the arity of each predicate
        for atom in p_e:
            arity.append(atom.arity)
            if not is_intensional(atom):
                raise ValueError(INTENSIONAL_REQUIRED_MESSAGE)

        if not is_intensional(target):
            raise ValueError(INTENSIONAL_REQUIRED_MESSAGE)
        arity.append(target.arity)

        self._target = target
        self._p_e = p_e
        self._arity = arity
        self._constants = list(constants)

    @property
    def target(self):
        return self._target

    @property
    def p_e(self):
        return self._p_e

    @property
    def arity(self):
        return self._arity

    @property
    def constants(self):
        return self._constants
