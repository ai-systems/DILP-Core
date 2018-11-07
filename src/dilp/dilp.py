'''Defines the main differentiable ILP code
'''

from src.ilp import ILP, Program_Template, Language_Frame, Rule_Template, Inference
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from src.core import Clause
import tensorflow as tf
import tensorflow.contrib.eager as tfe
import os
import numpy as np
import pandas as pd
from collections import OrderedDict


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

        # dictionary from predicates to rule weights matrices
        ilp = ILP(self.language_frame, self.background,
                  self.positive, self.negative, self.program_template)
        self.initial_valuation = ilp.convert()
        self.training_data = OrderedDict()  # index to label
        self.__init_training_data(positive, negative)
        self.base_valuation = []
        self.base_valuation_map = {}
        index = 0
        for val in self.initial_valuation:
            self.base_valuation.append(val)
            self.base_valuation_map[val[0]] = index
            index += 1
        self.base_valuation = np.array(self.base_valuation)

        # self.base_valuation = np.array(
        # [val[0] for val in self.initial_valuation], dtype=np.float32)
        self.generated = {}
        self.rule_weights = OrderedDict()
        self.__init__rule_weights()

    def __init_training_data(self, positive, negative):
        i = 0
        for val in self.initial_valuation:
            if val[0] in self.positive:
                self.training_data[i] = 1.0
            elif val[0] in self.negative:
                self.training_data[i] = 0.0
            i += 1

    def __init__rule_weights(self):
        with tf.variable_scope("rule_weights", reuse=tf.AUTO_REUSE):
            for p in [self.language_frame.target] + self.program_template.p_a:
                rule_manager = Optimized_Combinatorial_Generator(
                    self.program_template.p_a + [self.language_frame.target], self.program_template.rules[p], p, self.language_frame.p_e)
                self.generated[p] = rule_manager.generate_clauses()
                self.rule_weights[p] = tf.get_variable(p.predicate + "_rule_weights",
                                                       [len(self.generated[p][0]), len(
                                                           self.generated[p][1])],
                                                       initializer=tf.random_normal_initializer,
                                                       dtype=tf.float32)

    def inference_single_predicate(self, p, valuation, rule_weights):
        '''Train the model
        '''
        # convert ground atoms to initial evalutaions

        # Generate clauses for each intensional predicate
        # updated_f_c = {}

        memoize = {}
        c_p = []
        index = 0
        clause_map = {}
        generated = self.generated[p]
        for clause1 in generated[0]:
            (fc_1, memoize) = self.memoized_fc(
                memoize, clause1, valuation)
            for clause2 in generated[1]:
                (fc_2, memoize) = self.memoized_fc(
                    memoize, clause2, valuation)
                c_p_val = tf.zeros(len(self.base_valuation))
                for key in set(list(fc_1.keys()) + list(fc_2.keys())):
                    fc_1_i = 0
                    fc_2_i = 0
                    if key in fc_1:
                        fc_1_i = fc_1[key]
                    if key in fc_2:
                        fc_2_i = fc_2[key]
                    c_p_val[self.base_valuation_map[key]] = (
                        max(fc_1_i, fc_2_i))
                c_p.append(c_p_val)
                clause_map[index] = (clause1, clause2)
                index += 1
        rule_weights = tf.reshape(rule_weights, [-1])
        prob_rule_weights = tf.nn.softmax(rule_weights)[:, None]
        return (clause_map, tf.reduce_sum((tf.stack(c_p) * prob_rule_weights), axis=0))

    def inference_step(self, valuation):
        deduced_valuation = tf.zeros(len(self.initial_valuation))
        # deduction_matrices = self.rules_manager.deducation_matrices[predicate]
        for p in [self.language_frame.target] + self.program_template.p_a:
            deduced_valuation += self.inference_single_predicate(p,
                                                                 valuation,  self.rule_weights[p])
        return deduced_valuation + valuation - deduced_valuation * valuation

    def deduction(self):
        # takes background as input and return a valuation of target ground atoms
        valuation = self.base_valuation
        for _ in range(self.program_template.T):
            valuation = self.inference_step(valuation)
        return valuation

    def loss(self, batch_size=-1):
        labels = np.array(list(self.training_data.values())
                          [1], dtype=np.float32)
        outputs = tf.gather(self.deduction(), np.array(
            self.training_data.keys(), dtype=np.int32))
        if batch_size > 0:
            index = np.random.randint(0, len(labels), batch_size)
            labels = labels[index]
            outputs = tf.gather(outputs, index)
        loss = -tf.reduce_mean(labels * tf.log(outputs + 1e-10) +
                               (1 - labels) * tf.log(1 - outputs + 1e-10))
        return loss

    def grad(self):
        with tfe.GradientTape() as tape:
            loss_value = self.loss(-1)
            weight_decay = 0.0
            regularization = 0
            for weights in self.__all_variables():
                weights = tf.nn.softmax(weights)
                regularization += tf.reduce_sum(tf.sqrt(weights)
                                                ) * weight_decay
            loss_value += regularization / len(self.__all_variables())
        return tape.gradient(loss_value, self.__all_variables())

    def __all_variables(self):
        return [weights for weights in self.rule_weights.values()]

    def train(self, steps=300, name=None):
        """
        :param steps:
        :param name:
        :return: the loss history
        """
        str2weights = {str(key): value for key,
                       value in self.rule_weights.items()}
        if name:
            checkpoint = tfe.Checkpoint(**str2weights)
            checkpoint_dir = "./model/" + name
            checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
            try:
                checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
            except Exception as e:
                print(e)

        losses = []
        optimizer = tf.train.RMSPropOptimizer(learning_rate=0.5)

        for i in range(steps):
            grads = self.grad()
            optimizer.apply_gradients(zip(grads, self.__all_variables()),
                                      global_step=tf.train.get_or_create_global_step())
            loss_avg = float(self.loss().numpy())
            losses.append(loss_avg)
            print("-" * 20)
            print("step " + str(i) + " loss is " + str(loss_avg))
            # if i % 5 == 0:
            #     valuation_dict = self.valuation2atoms(self.deduction()).items()
            #     for atom, value in valuation_dict:
            #         print(str(atom) + ": " + str(value))
            #     if name:
            #         checkpoint.save(checkpoint_prefix)
            #         pd.Series(np.array(losses)).to_csv(name + ".csv")
            # print("-" * 20 + "\n")
        return losses

    def memoized_fc(self, memoize: dict, clause: Clause, valuation):
        '''Memoizing the clause f_c generation

        Arguments:
            memoize {[type]} -- [description]
            clause {[type]} -- [description]
        '''
        if clause is None:
            return ({}, memoize)
        if clause not in memoize:
            f_c = Inference.f_c(clause, valuation,
                                self.language_frame.constants)
            memoize[clause] = f_c
        return (memoize[clause], memoize)
