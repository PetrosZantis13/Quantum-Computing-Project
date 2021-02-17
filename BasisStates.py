'''
Quantum Computing Project
Author: Petros Zantis

The following class, ...
'''
import numpy as np

class BasisStates(object):
    
    '''
    Below is the constructor of the class, ...
    '''
    def __init__(self, dimension) :
        
        self.dimension = dimension
        vector_space = np.identity(dimension)
        
        bases = []
        for state in vector_space:
            basis = state.reshape(dimension,1)
            bases.append(basis)
            #print(basis)
        
        self.states = bases

# BasisStates(3)