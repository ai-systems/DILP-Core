'''Defines the clauses
'''
from src.core.atom import Atom


class Clause():

    def __init__(self, head: Atom, body: list):
        '''
        Arguments:
            head {Atom} -- Head atom of clause
            body {list} -- List of body atoms
        '''
        self._head = head
        self._body = body

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        self._head = value
