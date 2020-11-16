import sys

import pyparsing as pp

from src.core import Term, Atom
from src.ilp import Language_Frame, Program_Template, Rule_Template
from src.dilp import DILP
import tensorflow as tf
tf.compat.v1.enable_eager_execution()


# relationship will refer to 'track' in all of your examples
relationship = pp.Word(pp.alphas).setResultsName('relationship', listAllMatches=True)

number = pp.Word(pp.nums + '.')
variable = pp.Word(pp.alphas)
# an argument to a relationship can be either a number or a variable
argument = number | variable

# arguments are a delimited list of 'argument' surrounded by parenthesis
arguments = (pp.Suppress('(') + pp.delimitedList(argument) +
             pp.Suppress(')')).setResultsName('arguments', listAllMatches=True)

# a fact is composed of a relationship and it's arguments
# (I'm aware it's actually more complicated than this
# it's just a simplifying assumption)
fact = (relationship + arguments).setResultsName('facts', listAllMatches=True)

# a sentence is a fact plus a period
sentence = fact + pp.Suppress('.')

# self explanatory
prolog_sentences = pp.OneOrMore(sentence)


def process_file(filename):
    atoms = []
    predicates = set()
    constants = set()
    with open(filename) as f:
        data = f.read().replace('\n', '')
        result = prolog_sentences.parseString(data)
        for idx in range(len(result['facts'])):
            fact = result['facts'][idx]
            predicate = result['relationship'][idx]
            terms = [Term(False, term) for term in result['arguments'][idx]]
            term_var = [Term(True, f'X_{i}') for i in range(len(terms))]

            predicates.add(Atom(term_var, predicate))
            atoms.append(Atom(terms, predicate))
            constants.update([term for term in result['arguments'][idx]])
    return atoms, predicates, constants


B, pred_f, constants_f = process_file('%s/facts.dilp' % sys.argv[1])
P, target_p, constants_p = process_file(
    '%s/positive.dilp' % sys.argv[1])
N, target_n, constants_n = process_file(
    '%s/negative.dilp' % sys.argv[1])

if not (target_p == target_n):
    raise Exception('Positive and Negative files have different targets')
elif not len(target_p) == 1:
    raise Exception('Can learn only one predicate at a time')
elif not constants_n.issubset(constants_f) or not constants_p.issubset(constants_f):
    raise Exception(
        'Constants not in fact file exists in positive/negative file')


term_x_0 = Term(True, 'X_0')
term_x_1 = Term(True, 'X_1')

p_e = list(pred_f)
p_a = [Atom([term_x_0, term_x_1], 'pred')]
target = list(target_p)[0]
constants = constants_f

p_a_rule = (Rule_Template(1, False), None)
target_rule = (Rule_Template(0, False), Rule_Template(1, True))
rules = {p_a[0]: p_a_rule, target: target_rule}

langage_frame = Language_Frame(target, p_e, constants)
program_template = Program_Template(p_a, rules, 10)
dilp = DILP(langage_frame, B, P, N, program_template)
dilp.train()
