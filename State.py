'''
Quantum Computing Project
Author: Petros Zantis
'''
import numpy as np

class BasisStates():
    
    def __init__(self, dimension) :
        '''
        The constructor of the BasisStates class, which creates the 
        pure basis states with the given dimension.
        ''' 
        self.dimension = dimension
        vector_space = np.identity(dimension)
        self.vector = vector_space
        
        bases = []
        # also ensure bases are orthogonal?
                
        for state in vector_space:
            basis = state.reshape(dimension,1)
            bases.append(basis)
        
        self.states = bases

class State():
    
    def __init__(self, matrix) :
        '''
        The constructor of the State class, which takes as argument
        the matrix representing the quantum state.
        '''   
        self.vector = matrix   # vector representing the state
        
    def apply_gate(self, gate):
        '''
        Applies the gate given as argument to the quantum state
        '''  
        # ensure that the dimensions match
        assert(len(self.vector) == 2**(gate.qbitdim))   
        print(f"\nApplying the {gate.name} gate to state\n{self.vector}:\n")
        new_vector = gate.operator.dot(self.vector)
        self.vector = new_vector
    
    def probabilities(self):
        '''
        Calculates the amplitude of each basis state in an entangled state
        '''        
        basis_states = np.arange(0,len(self.vector),1)
        amps = []
        for basis in self.vector:
            amplitude = basis[0]
            amps.append(amplitude.conj() * amplitude)
        
        return basis_states, amps
            
class Qubit(State):
    
    def __init__(self, a, b) :
        '''
        The constructor of the Qubit class takes as argument the
        amplitudes a and b of basis states |0> and |1> respectively.
        '''  
        
        if(abs(a)**2 + abs(b)**2 != 1):
            print("wrong modulus")  # maybe use assert
        
        bases = BasisStates(2).states   # qubit is 2 dimensional
        basis0 = bases[0]
        basis1 = bases[1]
        
        self.vector = a*basis0 + b*basis1   # equation for state of a qubit

print("An example of Basis States:")
print(BasisStates(4).vector)      
print(Qubit(0.8,0.6).probabilities())