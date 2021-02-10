# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:35:20 2021

@author: mikva
"""
import QuantumRegister
import numpy as np
import SquareMatrix as sm

class QuantumCircuit:
    def __init__(self, size):
        """
        Initiates the quantum circuit.

        Parameters
        ----------
        reg : QuantumRegister object
            The quantum register to be made into a circuit.

        Returns
        -------
        None.
        """
        self.singlegates = {'x' : np.array([[0,1], [1,0]]),
                      'y' : np.array([[0,-1j], [1j,0]]),
                      'z' : np.array([[1,0], [0,-1]]),
                      'h' : np.array([[1,1],[1,-1]])/np.sqrt(2),
                      'p' : np.array([[1,0],[0,1j]]),
                      't' : np.array([[1,0],[0,np.exp(1j*np.pi/4)]]),
                      'i' : np.eye(2)
                      }
        self.register = QuantumRegister.QuantumRegister(size)
        self.gates = []
        for i in range(self.register.Qbits.size):
            self.gates.append(['i'])
        self.gateindex = 0
        
    def addGate(self, gate, bits):
        """
        Adds an arbitrary gate to the set of gates stored in the circuit

        Parameters
        ----------
        gate : char
            The type of gate to be added. Current options are:'x', 'y', 'z', 'h', 'p', 't'
        
        bits : array_like
            The position of bits the gate is needed to be added
            
        Returns
        -------
        None.

        """
        # Check availability
        available = True
        for i in bits: 
            if self.gates[i][self.gateindex]!='i':
                available = False
        if available:
            for i in bits:
                self.gates[i][self.gateindex] = gate
        else:
            for i in range(len(self.gates)): # Go through all rows of self.gates and add in the gate if needed, add in 'i' if not needed
                if i in bits:
                    self.gates[i].append(gate)
                else:
                    self.gates[i].append('i')
            self.gateindex += 1
        
    def x(self, bits):
        self.addGate('x', bits)
    
    def y(self, bits):
        self.addGate('y', bits)
    
    #Pls someone else do the rest
        
    def r(self, bits, theta):
        self.addGate(('r', theta), bits)
    
    def makeMatrices(self):
        """
        Creates the matrices that will be applied to the wavevector

        Returns
        -------
        bigmats : numpy array
            list of np matrices that will be applied to the statevector

        """
        gates = np.array(self.gates, dtype = object).T
        
        #debug
        #print(gates)
        
        bigmats = []
        for i, slot in enumerate(gates):
            bigmat = sm.SparseMatrix(1, [(0,0,1)])
            for j in slot:
                if type(j)==tuple:
                    r = self.Rt(j[1])
                    bigmat = r.outer(bigmat)
                else: bigmat = sm.toSparse(self.singlegates[j]).tensorProd(bigmat)
            bigmats.append(bigmat)
        
        return np.array(bigmats)
    
    def Rt(self, theta):
        return sm.toSparse(np.array([[1, 0], [0, np.exp(1j*theta)]]))
        
    def simulate(self):
        """
        Applies the circuit to the initialized statevector

        Returns
        -------
        The final state of the state vector
        Planned: any measurements throughout the experiment
        
        """
        operations = self.makeMatrices()
        for operation in operations:
            self.register.Statevec = operation.Apply(self.register.Statevec)
            print(self.register)
        
        
    
if __name__ == '__main__':
    pass