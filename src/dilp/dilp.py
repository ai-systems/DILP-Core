'''Defines the main differentiable ILP code
'''

from src.ilp import ILP, Program_Template, Language_Frame, Rule_Template, Inference
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from src.core import Clause


class DILP():

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

    def train(self):
        '''Train the model
        '''
        # convert ground atoms to initial evalutaions
        ilp = ILP(self.language_frame, self.background,
                  self.positive, self.negative, self.program_template)
        initial_valuation = ilp.convert()
        # Generate clauses for each intensional predicate
        generated_clause = {}
        for p in [self.language_frame.target] + self.program_template.p_a:
            rule_manager = Optimized_Combinatorial_Generator(
                self.program_template.p_a + [self.language_frame.target], self.program_template.rules[p], p, self.language_frame.p_e)
            generated = rule_manager.generate_clauses()
            memoize = {}
            for clause1 in generated[0]:
                for clause2 in generated[1]:
                    fc_1 = self.memoized_fc(
                        memoize, clause1, initial_valuation)
                    fc_2 = self.memoized_fc(
                        memoize, clause2, initial_valuation)
                    print(fc_1)

    def memoized_fc(self, memoize: dict, clause: Clause, valuation):
        '''Memoizing the clause f_c generation

        Arguments:
            memoize {[type]} -- [description]
            clause {[type]} -- [description]
        '''
        if clause not in memoize:
            f_c = Inference.f_c(clause, valuation,
                                self.language_frame.constants)
            memoize[clause] = f_c
        return (memoize[clause], memoize)
