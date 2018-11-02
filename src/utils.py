'''Defines stateless utility functions
'''
from src.core import Atom


def is_intensional(atom: Atom):
    '''Checks if the atom is intensional. If true returns true, otherwise returns false

    Arguments:
        atom {Atom} -- Atom to be analyzed
    '''
    for term in atom.terms:
        if not term.isVariable:
            return False

    return True


INTENSIONAL_REQUIRED_MESSAGE = 'Atom is not intensional'
