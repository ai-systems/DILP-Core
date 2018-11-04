'''Defines the atom class
'''
import collections


class Atom():
    def __init__(self, terms: list, predicate: str):
        '''
        Arguments:
            terms {list} -- List of of terms defining atom
            name {str} -- name of the predicate
        '''
        self._terms = terms
        self._predicate = predicate
        self._variables = set([term.name for term in terms])

    def __str__(self):
        return "%s(%s)" % (self._predicate, ','.join([str(name) for name in self._terms]))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self._terms == other.terms and self._predicate == other.predicate

    def __hash__(self):
        return hash(str(self))

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, value):
        self._terms = value

    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        self._predicate = value

    @property
    def arity(self):
        return len(self._terms)

    @property
    def variables(self):
        return self._variables

    def is_same_predicate(self, other):
        '''Checks equality of predicate

        Arguments:
            other {Atom} -- Atom to check predicate equality
        '''

        return self._predicate == other.predicate
