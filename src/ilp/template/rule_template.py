'''Defines the rule template
'''


class Rule_Template():

    def __init__(self, v: int, allow_intensional: bool):
        '''

        Arguments:
            v {int} -- numberof existentially quantified variable allowed in the clause
            allow_intensional {bool} -- True is intensional predicates are allowed, False if only extensional predicates
        '''

        self._v = v
        self._allow_intensional = allow_intensional

    @property
    def v(self):
        return self._v

    @property
    def allow_intensional(self):
        return self._allow_intensional
