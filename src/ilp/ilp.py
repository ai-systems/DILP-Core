'''Defines the ILP problem
'''

from src.ilp import Language_Frame, Program_Template
from src.core import Atom, Term


class ILP():

    def __init__(self, language_frame: Language_Frame, background: list, positive: list, negative: list, program_template: Program_Template):
        '''
        Arguments:
            language_frame {Language_Frame} -- language frame
            background {list} -- background assumptions
            positive {list} -- positive examples
            negative {list} -- negative examples
            program_template {Program_Template} -- program template
        '''
        self.language_frame = language_frame
        self.background = background
        self.positive = positive
        self.negative = negative
        self.program_template = program_template

    def generate_ground_atoms(self):
        '''Generates the ground atoms from p_i,p_a,target and constants
        '''
        p = list(set(self.language_frame.p_e +
                     self.program_template.p_a + [self.language_frame.target]))
        constants = self.language_frame.constants

        # Build constant matrix
        constant_matrix = []
        for const1 in constants:
            for const2 in constants:
                term1 = Term(False, const1)
                term2 = Term(False, const2)
                constant_matrix.append([term1, term2])
        # Build ground atoms
        ground_atoms = []
        ground_atoms.append(Atom([], '⊥'))
        for pred in p:
            for term in constant_matrix:
                ground_atoms.append(Atom(term, pred.predicate))
        return ground_atoms

    def convert(self):
        '''Generate initial valuations
        '''
        ground_atoms = self.generate_ground_atoms()
        initial_valuation = []
        for atom in ground_atoms:
            if atom in self.background:
                initial_valuation.append((atom, 1))
            else:
                initial_valuation.append((atom, 0))
        return initial_valuation
