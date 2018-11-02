'''Defines the atom class
'''


class Atom():
    def __init__(self, terms: list, predicate: str):
        '''
        Arguments:
            terms {list} -- List of of terms defining atom
            name {str} -- name of the predicate
        '''
        self._terms = terms
        self._predicate = predicate

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
