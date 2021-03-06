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
        for state in vector_space:
            basis = state.reshape(dimension,1)
            bases.append(basis)
        
        self.states = bases

class State():
    
    # PETRO CHECK THAT ALWAYS NORMALISED LIKE QUBIT
    
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
        #print(f"\nApplying the {gate.name} gate to state\n{self.vector}:\n")
        new_vector = gate.operator.dot(self.vector)
        self.vector = new_vector
    
    def probabilities(self):
        '''
        Calculates the amplitude of each basis state in an entangled state
        '''        
        basis_states = []
        amps = []
        for basis, amplitude in enumerate(self.vector):
            basis_states.append(basis)
            amp = amplitude[0]
            amps.append(amp.conj() * amp)
        
        print(f"The amplitudes sum up to : {np.sum(amps):.2f}")  # must be 1 for a normalised state
        
        return basis_states, amps
    
    def measure(self):
        '''
        Measures the quantum state and collapses it to one of its basis states.
        '''        
        basis_states, amps = self.probabilities()
        r = np.random.random()     
        
        for basis, value in enumerate(amps):
            if(r < (value)):
                collapsed = basis
                print(f"Collapsed to {collapsed}")
                break
            else:
                r -= value
                
        self.vector = BasisStates(len(basis_states)).states[collapsed]
        return collapsed
            
class Qubit(State):
    
    def __init__(self, a, b) :
        '''
        The constructor of the Qubit class takes as argument the
        amplitudes a and b of basis states |0> and |1> respectively.
        '''  
        self.a = a
        self.b = b
        
        if(abs(a)**2 + abs(b)**2 != 1):
            print("Unnormalised modulus")  # maybe use assert
        
        bases = BasisStates(2).states   # qubit is 2 dimensional
        basis0 = bases[0]
        basis1 = bases[1]
        
        self.vector = self.a*basis0 + self.b*basis1   # equation for state of a qubit
        