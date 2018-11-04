"""Defines the ILP 
"""
from src.ilp.language_frame import Language_Frame
from src.ilp.template import Rule_Template, Program_Template
from src.ilp.rule_manager import Rule_Manger
from src.ilp.Inference import Inference


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

    def convert(self):
        '''Generate initial valuations
        '''
        inference = Inference(self.program_template, self.language_frame)
        ground_atoms = inference.generate_ground_atoms()
        initial_valuation = []
        for atom in ground_atoms:
            if atom in self.background:
                initial_valuation.append((atom, 1))
            else:
                initial_valuation.append((atom, 0))
        return initial_valuation
