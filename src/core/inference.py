'''Class for performing the forward chain inference
'''

from src.core.atom import Atom
from src.core.clause import Clause
from src.core.term import Term
from itertools import product

class Inference():

    def __init__(self, language_frame, program_template):
        self.constants = ""

    def inference(self, max_steps : int, initial_valuation : list, clauses : list):
        '''
        Arguments:
            max_steps {int} -- max number of inference steps
            initial_valuation {list} -- the output of the initial valuation
            clauses {list} -- list of generated clauses 
        '''
        #repeat this for max_setps
        for clause in clauses:
            #apply the clause to the ground atoms
            apply_rule(clause, initial_valuation)
        return " "

    def generate_inductive_matrix(self, clause, atoms):
        matrix = []
        for atom in atoms:
            if clause.head.predicate == atom.predicate:
                matrix.append(self.find_satisfy(clause, atom, atoms))
            else:
                matrix.append([])
        print(matrix)

    def find_satisfy(self, clause, head, ground_atoms):
        
        term1 = Term(True, 'X')
        term2 = Term(True, 'Z')
        term3 = Term(True, 'Y')
        q = Term (True, "Q")
        atom1 = Atom([term1, term3], 'R')
        atom2 = Atom([term1, term2], 'P')
        atom3 = Atom([term2, term3], 'Q')
        clause = Clause(atom1, [atom2, atom3])
        self.constants = ["a","b"]
        term4 = Term(False, "a")
        term5 = Term(False, "b")
        
        head = Atom([term4,term5],'R')
        ground_atoms = [Atom([term4,term4],'P'), Atom([term4,term5],'P'), Atom([term5,term4],'P'), Atom([term5,term5],'P'), Atom([term4,term4],'Q'), Atom([term4,term5],'Q'), 
                        Atom([term5,term4],'Q'), Atom([term5,term5],'Q'), Atom([term4,term4],'R'), Atom([term4,term5],'R'), Atom([term5,term4],'R'), Atom([term5,term5],'R')]
        
        # given (y1,y2) a pair of indexes identifying ground atoms. 
        # if c = a <= a1, a2 then satisfies_c(y1,y2) is true if there is a substitution theta
        # such that a1[theta] = y1 a2[theta] = y2
        # find all the pairs (y1,y2) that satisfy head
        
        fixed_variables = []
        fixed_substitutions = {}
        free_variables = []
        free_substitutions = []

        for variable in clause.head.terms:
            fixed_variables.append(variable.name)
            fixed_substitutions[variable.name] = head.terms[clause.head.terms.index(variable)].name
        
        for atom in clause.body:
            for variable in atom.terms:
                if not variable.name in fixed_variables and not variable.name in free_variables:
                    free_variables.append(variable.name)
                    p = product(variable.name, self.constants)
                    temp = []
                    for obj in p:
                        temp.append(obj)
                    free_substitutions.append(temp)

        comb_substitution = []
        if len(free_substitutions) > 1:
            p = product(*free_substitutions)
            for obj in p:
                sub_dic = {}
                for entry in obj:
                    sub_dic[entry[0]] = entry[1]
                comb_substitution.append(sub_dic)
        else:
            for obj in free_substitutions[0]:
                comb_substitution.append({obj[0]:obj[1]})

        print("constants", self.constants)
        print("fixed variables", fixed_variables)
        print("fixed substitutions", fixed_substitutions)
        print("free variables", free_variables)
        print("free substitutions", comb_substitution)

        
        for substitution in comb_substitution:
            print("sub", substitution)
            i = 0
            for ground_atom in ground_atoms:
                if ground_atom.predicate == head.predicate:
                    continue
                for atom in clause.body:
                    if ground_atom.predicate == atom.predicate:    
                        #check valid substitution
                        flag = True
                        for term in atom.terms:
                            if term.name in fixed_substitutions:
                                if fixed_substitutions[term.name] != ground_atom.terms[atom.terms.index(term)].name:
                                    flag = False
                            elif substitution[term.name] != ground_atom.terms[atom.terms.index(term)].name:
                                flag = False
                        if flag == True:
                            print("found", ground_atom.predicate, i)
                i += 1


        