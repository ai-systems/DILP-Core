'''Defines the main differentiable ILP code
'''

from src.ilp import ILP, Program_Template, Language_Frame, Rule_Template, Inference
from src.ilp.generate_rules import Optimized_Combinatorial_Generator
from src.core import Clause
import tensorflow as tf
from collections import OrderedDict
import numpy as np
from src.utils import printProgressBar
#import tensorflow.contrib.eager as tfe # obsolete in TF2
import os


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
        self.training_data = OrderedDict()  # index to label
        self.__init__parameters()

    def __init__parameters(self):
        self.rule_weights = OrderedDict()
        ilp = ILP(self.language_frame, self.background,
                  self.positive, self.negative, self.program_template)
        (valuation, valuation_mapping) = ilp.convert()
        self.valuation_mapping = valuation_mapping
        self.base_valuation = valuation
        self.deduction_map = {}
        self.clause_map = {}
        with tf.compat.v1.variable_scope("rule_weights", reuse=tf.compat.v1.AUTO_REUSE):
            for p in [self.language_frame.target] + self.program_template.p_a:
                rule_manager = Optimized_Combinatorial_Generator(
                    self.program_template.p_a + [self.language_frame.target], self.program_template.rules[p], p, self.language_frame.p_e)
                generated = rule_manager.generate_clauses()
                self.clause_map[p] = generated
                self.rule_weights[p] = tf.compat.v1.get_variable(p.predicate + "_rule_weights",
                                                       [len(generated[0]), len(
                                                           generated[1])],
                                                       initializer=tf.compat.v1.random_normal_initializer,
                                                       dtype=tf.float32)
                deduction_matrices = []
                elm1 = []
                for clause1 in generated[0]:
                    elm1.append(Inference.x_c(
                        clause1, valuation_mapping, self.language_frame.constants))
                elm2 = []
                for clause2 in generated[1]:
                    elm2.append(Inference.x_c(
                        clause2, valuation_mapping, self.language_frame.constants))
                deduction_matrices.append((elm1, elm2))
                self.deduction_map[p] = deduction_matrices
        for atom in valuation_mapping:
            if atom in self.positive:
                self.training_data[valuation_mapping[atom]] = 1.0
            elif atom in self.negative:
                self.training_data[valuation_mapping[atom]] = 0.0

    def __all_variables(self):
        return [weights for weights in self.rule_weights.values()]

    def show_atoms(self, valuation):
        result = {}
        for atom in self.valuation_mapping:
            if atom in self.positive:
                print('%s Expected: 1 %.3f' %
                      (str(atom), valuation[self.valuation_mapping[atom]]))
            elif atom in self.negative:
                print('%s Expected: 0 %.3f' %
                      (str(atom), valuation[self.valuation_mapping[atom]]))

    def show_definition(self):
        for predicate in self.rule_weights:
            shape = self.rule_weights[predicate].shape
            rule_weights = tf.reshape(self.rule_weights[predicate], [-1])
            weights = tf.reshape(tf.nn.softmax(rule_weights)[:, None], shape)
            print('----------------------------')
            print(str(predicate))
            clauses = self.clause_map[predicate]
            pos = np.unravel_index(
                np.argmax(weights, axis=None), weights.shape)
            print(clauses[0][pos[0]])
            print(clauses[1][pos[1]])

            '''
            for i in range(len(indexes[0])):
                if(weights[indexes[0][i], indexes[1][i]] > max_weights):
                    max_weights = weights[indexes[0][i],
                                          indexes[1][i]] > max_weights
                print(clauses[0][indexes[0][i]])
                print(clauses[1][indexes[1][i]])
            '''
            print('----------------------------')

    def train(self, steps=501, name='test'):
        """
        :param steps:
        :param name:
        :return: the loss history
        """
        str2weights = {str(key): value for key,
                       value in self.rule_weights.items()}
        # if name:
        #     checkpoint = tf.train.Checkpoint(**str2weights)
        #     checkpoint_dir = "./model/" + name
        #     checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
        #     try:
        #         checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
        #     except Exception as e:
        #         print(e)

        losses = []
        optimizer = tf.compat.v1.train.RMSPropOptimizer(learning_rate=0.05)

        for i in range(steps):
            grads = self.grad()
            optimizer.apply_gradients(zip(grads, self.__all_variables()),
                                      global_step=tf.compat.v1.train.get_or_create_global_step())
            loss_avg = float(self.loss().numpy())
            losses.append(loss_avg)
            print("-" * 20)
            print("step " + str(i) + " loss is " + str(loss_avg))
            if i % 5 == 0:
                # self.show_definition()
                self.show_atoms(self.deduction())
                self.show_definition()
                # if name:
                # checkpoint.save(checkpoint_prefix)
                # pd.Series(np.array(losses)).to_csv(name + ".csv")
            print("-" * 20 + "\n")
        return losses

    def loss(self, batch_size=-1):
        labels = np.array(
            [val for val in self.training_data.values()], dtype=np.float32)
        keys = np.array(
            [val for val in self.training_data.keys()], dtype=np.int32)
        outputs = tf.gather(self.deduction(), keys)
        if batch_size > 0:
            index = np.random.randint(0, len(labels), batch_size)
            labels = labels[index]
            outputs = tf.gather(outputs, index)
        loss = -tf.reduce_mean(input_tensor=labels * tf.math.log(outputs + 1e-10) +
                               (1 - labels) * tf.math.log(1 - outputs + 1e-10))
        return loss

    def grad(self):
        with tf.GradientTape() as tape:
            loss_value = self.loss(-1)
            weight_decay = 0.0
            regularization = 0
            for weights in self.__all_variables():
                weights = tf.nn.softmax(weights)
                regularization += tf.reduce_sum(input_tensor=tf.sqrt(weights)
                                                ) * weight_decay
            loss_value += regularization / len(self.__all_variables())
        return tape.gradient(loss_value, self.__all_variables())

    @staticmethod
    def update_progress(progress):
        print('\r[{0}] {1}%'.format('#' * (int(progress) / 10), progress))

    def deduction(self):
        # takes background as input and return a valuation of target ground atoms
        valuation = self.base_valuation
        print('Performing Inference')
        for step in range(self.program_template.T):
            printProgressBar(step, self.program_template.T, prefix='Progress:',
                             suffix='Complete', length=50)
            valuation = self.inference_step(valuation)
        print('Inference Complete')
        return valuation

    def inference_step(self, valuation):
        deduced_valuation = tf.zeros(valuation.shape[0])
        # deduction_matrices = self.rules_manager.deducation_matrices[predicate]
        for predicate in self.deduction_map:
            for matrix in self.deduction_map[predicate]:
                deduced_valuation += DILP.inference_single_predicate(
                    valuation, matrix, self.rule_weights[predicate])
        return deduced_valuation + valuation - deduced_valuation * valuation

    @staticmethod
    def inference_single_predicate(valuation, deduction_matrices, rule_weights):
        '''
        :param valuation:
        :param deduction_matrices: list of list of matrices
        :param rule_weights: list of tensor, shape (number_of_rule_temps, number_of_clauses_generated)
        :return:
        '''
        result_valuations = [[], []]
        for i in range(len(result_valuations)):
            for matrix in deduction_matrices[i]:
                result_valuations[i].append(
                    DILP.inference_single_clause(valuation, matrix))

        c_p = []  # flattened
        for clause1 in result_valuations[0]:
            for clause2 in result_valuations[1]:
                c_p.append(tf.maximum(clause1, clause2))

        rule_weights = tf.reshape(rule_weights, [-1])
        prob_rule_weights = tf.nn.softmax(rule_weights)[:, None]
        return tf.reduce_sum(input_tensor=(tf.stack(c_p) * prob_rule_weights), axis=0)

    @staticmethod
    def inference_single_clause(valuation, X):
        '''
        The F_c in the paper
        :param valuation:
        :param X: array, size (number)
        :return: tensor, size (number_of_ground_atoms)
        '''
        X1 = X[:, :, 0, None]
        X2 = X[:, :, 1, None]
        Y1 = tf.gather_nd(params=valuation, indices=X1)
        Y2 = tf.gather_nd(params=valuation, indices=X2)
        Z = Y1 * Y2
        return tf.reduce_max(input_tensor=Z, axis=1)
