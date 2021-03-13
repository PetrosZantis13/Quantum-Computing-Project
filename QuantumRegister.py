"""
add a description here of the module

"""
import numpy as np
import Sparse


class QuantumRegister:
    """ 
    Initializes the quantum register of length n. Creates a list of default qubits
    in state 0 and initializes the wavevector which describes the register.

    :param n: (int) length of register

    """
    def __init__(self, n):
        Qbits = []

        for i in range(n): 
            Qbits.append(Qubit())
        self.Qbits = np.array(Qbits)
        self.initialize()        

    def __str__(self):        
        toPrint = ''

        toPrint += '\n'
        for i in range(self.Statevec.Elements.size):
            toPrint += f'|{i}> = {((self.Statevec.Elements[i])*np.conj(self.Statevec.Elements[i])).real}\n'
        
        return toPrint
    
    def initialize(self):
        """
        Sets the statevector according to the current state of qubits
        """
        self.Statevec = Sparse.Vector(np.array([1], dtype=complex))
        for qbit in self.Qbits[::-1]:
            self.Statevec = self.Statevec.outer(qbit.vals)
            
    def setStateVec(self, newVec):
        """
        Allows the user to set the state vector to a new vector. Automatically normalises the vector.
        
        :param newVec: (list) The new vector to become the state vector

        """
        newVec = np.array(newVec, dtype=complex)
        assert self.Statevec.Dimension == newVec.size, 'Wrong dimensions for new statevector'
        normal_const = np.sqrt((newVec*newVec.conj()).sum())
        self.Statevec = Sparse.Vector(newVec/normal_const)
        
    def setQbits(self, qbits, vals):
        """
        Sets the initial values of the qubits if required,
        although it is preferred to use gates for this step.
        Automatically normalizes the Qbit

        :param qbits: (list) qubts to be set
        :param vals: (list) The values that the qubits should be set to. Each entry containing two values
        """
        
        for qbit in qbits:
            self.Qbits[qbit].vals = Sparse.Vector(np.array(vals[qbit]) / np.linalg.norm(vals[qbit]))
        self.initialize()

    def measure(self):
        """
        Attempts to measure the current statevector in terms of individual qubits
        """
        for qbit in self.Qbits:
            qbit.vals.Elements[1] = 0+0j
        for i, value in enumerate(self.Statevec.Elements):
            for j, qbit in enumerate(self.Qbits):
                if ((i>>(j)) & 1) == 1:
                    #print(i,j,value)
                    qbit.vals.Elements[1] += value*value.conj()
        for qbit in self.Qbits:
            qbit.vals.Elements[0] = complex(1 - qbit.vals.Elements[1])
            qbit.normalize()
            
class Qubit:
    """
    Creates a qubit using sparse matrices.
    """
    def __init__(self):
        self.vals = Sparse.Vector(np.array([1.+0.j, 0.+0.j]))
    
    def normalize(self):
        """Normalizes all the elements."""
        self.vals.Elements = self.vals.Elements / np.sqrt((self.vals.Elements*self.vals.Elements.conj()).sum())
    
    def get0(self):
        """Gets the 0 state"""
        return self.vals.Elements[0]
    
    def get1(self):
        """Gets the 1 state"""
        return self.vals.Elements[1]
    
    def __str__(self):
        """Printing function"""
        toPrint = ''
        toPrint += f'|0> = {self.vals.Elements[0]} \n'
        toPrint += f'|1> = {self.vals.Elements[1]} \n'
        
        return toPrint
        

if __name__ == '__main__':
    pass
    