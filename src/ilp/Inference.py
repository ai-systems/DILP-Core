'''Defines the inference
'''
from src.core import Atom
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from src.ilp import Program_Template, Language_Frame
from src.core import Atom, Term, Clause


class Inference():

    def __init__(self, program_template: Program_Template, language_frame: Language_Frame):
        '''
        Arguments:
            program_template {Program_Template} -- program template
            language_frame {Language_Frame} -- language frame used
        '''
        self.program_template = program_template
        self.language_frame = language_frame

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
        for pred in p:
            for term in constant_matrix:
                ground_atoms.append(Atom(term, pred.predicate))
        ground_atoms.append(Atom([], '⊥'))
        return ground_atoms
