'''Defines the Term clas
'''


class Term():

    def __init__(self, isVariable: bool, name: str):
        '''
        Arguments:
            isVariable {bool} -- is this term a variable or a constant
            name {string} -- id of variable/constant
        '''
        self._isVariable = isVariable
        self._name = name

    def __str__(self):
        return self._name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self._isVariable == other.isVariable and self._name == other.name

    def __hash__(self):
        return hash(str(self))

    @property
    def isVariable(self):
        return self._isVariable

    @isVariable.setter
    def isVariable(self, value):
        self._isVariable = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
