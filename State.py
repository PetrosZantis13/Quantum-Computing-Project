'''
The State module is used to create objects representing quantum states. 
'''
import numpy as np

class BasisStates():
    """ creates the pure basis states with the given dimension.

    :param dimension: (int) dimensions of vector space

    """
    
    def __init__(self, dimension) :
        self.dimension = dimension
        vector_space = np.identity(dimension)
        self.vector = vector_space
        
        bases = []                
        for state in vector_space:
            basis = state.reshape(dimension,1)
            bases.append(basis)
        
        self.states = bases

class State():
    """ General Method of creating objects that represent quantum states

    :param matrix:  (array) Matrix representing Quantum State
    """
        
    def __init__(self, matrix) :
        # vector representing the state
        self.vector = matrix 
        
    def apply_gate(self, gate):
        '''
        Applies the gate given as argument to the quantum state
        After asserting that the dimensions of the state and gate match, 
        calculates the dot product of the gate’s operator and the state’s vector,
        and saves the result as the new updated state vector.

        :param gate:  (array) gate of the circuit

        '''  
        # ensure that the dimensions match
        assert(len(self.vector) == 2**(gate.qbitdim))   
        new_vector = gate.operator.dot(self.vector)
        self.vector = new_vector
    
    def probabilities(self):
        '''
        Calculates the amplitude of each basis state in an entangled state
        Goes through the amplitudes of each basis, multiplies it by its 
        conjugate, and outputs a list of the basis states and their 
        corresponding probabilities inside the state vector. 

        :return: (list) basis states and their probabilities inside the state vector
        
        '''        
        basis_states = []
        amps = []
        for basis, amplitude in enumerate(self.vector):
            basis_states.append(basis)
            amp = amplitude[0]
            amps.append(amp.conj() * amp)

        # must be 1 for a normalised state
        print(f"The amplitudes sum up to : {np.sum(amps):.2f}")
        
        return basis_states, amps
    
    def measure(self):
        '''
        Measures the quantum state and collapses it to one of its basis states.
        Collapses the wavefunction to one of its basis states by using the probabilities
        from the the method of the probabilities function and the numpy 
        random library.

        :return: (int) index of collapsed state
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
    """Subclass of the State class. Qubits are specifically 2 dimensional states. 
    Builds the state vector. 
    
    :param a: (int) amplitude of basis state |0>
    :param b: (int) amplitude of basis state |1>

    """ 
    
    def __init__(self, a, b) :
        self.a = a
        self.b = b
        
        if(abs(a)**2 + abs(b)**2 != 1):
            print("Unnormalised modulus")  # maybe use assert
        
        bases = BasisStates(2).states   # qubit is 2 dimensional
        basis0 = bases[0]
        basis1 = bases[1]
        
        self.vector = self.a*basis0 + self.b*basis1   # equation for state of a qubit
        