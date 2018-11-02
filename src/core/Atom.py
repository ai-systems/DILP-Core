'''Defines the atom class
'''


class Atom():
    def __init__(self, terms: list, name: str):
        '''
        Arguments:
            terms {list} -- List of of terms defining atom
            name {str} -- name of the predicate
        '''
        self._terms = terms
        self._name = name

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, value):
        self._terms = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
