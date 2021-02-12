# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import QuantumRegister
import SquareMatrix
import numpy as np

if __name__ == '__main__':
    
    circuit = QuantumCircuit.QuantumCircuit(5)
    circuit.addGate('x', [4])
    circuit.addGate('h', [0,1])
    circuit.addGate('h', [3])
    
    print(np.array(circuit.gates, dtype = object))
    print(circuit.register)
    circuit.simulate()
    #print(circuit.makeMatrices())
    """
    identity = np.array([[1,0],[0,1]])
    print(type(identity)==np.ndarray)
    print(SquareMatrix.toSparse(identity))
    """