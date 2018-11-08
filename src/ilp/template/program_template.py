'''Descirbe the range programs that can be generated
'''

from src.utils import is_intensional, INTENSIONAL_REQUIRED_MESSAGE


class Program_Template():

    def __init__(self, p_a: list, rules: dict, T: int):
        '''
        Arguments:
            p_a {list} -- set of auxiliary predicates; these are the additional invented predicates used to help define the target predicate
            rules {tuple} -- Map of intensional predicate to a pair if rule templates 
            T {int} -- Max number of steps of forward chaining inference
        '''
        arity = []  # Specifying the arity of each auxiliary predicate
        for atom in p_a:
            if not is_intensional(atom):
                raise ValueError(INTENSIONAL_REQUIRED_MESSAGE)
            arity.append(atom.arity)

        self._p_a = p_a
        self._rules = rules
        self._T = T
        self._arity = arity

    @property
    def p_a(self):
        return self._p_a

    @property
    def rules(self):
        return self._rules

    @property
    def T(self):
        return self._T

    def arity(self):
        return self._arity
