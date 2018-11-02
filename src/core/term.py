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
