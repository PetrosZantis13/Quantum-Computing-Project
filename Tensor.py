'''
Quantum Computing Project
Author: Petros Zantis
'''
import numpy as np

class Tensor(object):

    def __init__(self, inputs) :
        
        '''
        The constructor of the Tensor class takes as argument a list of the inputs 
        and calculates their outer product from right to left (order of applying them)
        '''
        
        self.inputs = inputs 
        
        product = inputs[-1]
        for i in range(len(self.inputs)-2,-1,-1):
            # assert dimensions of inputs are equals
            product = np.kron(self.inputs[i], product)
        
        self.product = product 
    
