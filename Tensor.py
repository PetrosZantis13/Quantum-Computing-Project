'''
Quantum Computing Project
Author: Petros Zantis
'''
import numpy as np
import State
import Gate

class Tensor(object):

    def __init__(self, inputs) :        
        '''
        The constructor of the Tensor class takes as argument a list of the inputs
        '''        
        assert isinstance(inputs, list), "Inputs must be a list"    
        self.inputs = inputs   
        
    def calculate(self):   
        '''
        A function to calculate the outer product based on the given inputs
        ordered from right to left (order of applying them)
        '''
        
        if(all(isinstance(state, State.State) for state in self.inputs)):
            # Tensor product of states
            product = self.inputs[-1].vector
            for i in range(len(self.inputs)-2,-1,-1):
                product = np.kron(self.inputs[i].vector, product)
                
        elif(all(isinstance(gate, Gate.Gate) for gate in self.inputs)):
            # Tensor product of gates
            product = self.inputs[-1].operator
            for i in range(len(self.inputs)-2,-1,-1):
                product = np.kron(self.inputs[i].operator, product)
        else:
            print("Incompatible inputs!")
            
        self.product = product