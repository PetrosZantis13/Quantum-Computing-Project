'''
Quantum Computing Project
Author: Petros Zantis

The following class, Register, 
'''
import numpy as np

class TensorProduct(object):
    
    '''
    Below is the constructor of the class,
    '''
    def __init__(self, inputs) :
        
        self.inputs = inputs 
        
        product = inputs[-1]
        for i in range(len(self.inputs)-2,-1,-1):
            product = np.kron(self.inputs[i], product)
        
        self.product = product 
    
