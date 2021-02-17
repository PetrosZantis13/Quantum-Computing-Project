'''
Quantum Computing Project
Author: Petros Zantis

The following class, Qubit, ...
'''
import numpy as np
from BasisStates import BasisStates

class Qubit(object):
    
    '''
    Below is the constructor of the class, ...
    '''
    def __init__(self, a, b) :  # give the basis explicitly or just create them in the constructor?
        
        self.a = a
        self.b = b
        
        if(abs(self.a)**2 + abs(self.b)**2 != 1):
            print("wrong modulus")
        
        # also ensure bases are orthogonal?
        
        bases = BasisStates(2).states
        basis0 = bases[0]
        basis1 = bases[1]
        
        self.vector = a*basis0 + b*basis1        
    
    '''
    maybe getters and setters here 
    + modulus checker (always ==1)
    '''
        
    def apply_gate(self, gate):    
        
        assert(gate.qbitdim == 1)   # ensure that its a single qubit gate
        print(f"\nApplying the {gate.name} gate to qubit\n{self.vector}:\n")
        new = gate.operator.dot(self.vector)
        self.vector = new


# print(Qubit(0.8,0.6).vector)
# print(Qubit(0.9,0.6).vector)