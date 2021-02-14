# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import QuantumRegister
import SquareMatrix as sm
import numpy as np

if __name__ == '__main__':
    
    circuit = QuantumCircuit.QuantumCircuit(3)
    circuit.addGate('x', [0])
    circuit.addBigGate(('cn', 0, 2))
    
    #print(circuit.cNot((0,2)).toDense())
    
    
    
    #print(np.array(circuit.gates, dtype = object))
    #print(circuit.register)
    #circuit.simulate()
    circuit.show()
    """
    identity = np.array([[1,0],[0,1]])
    print(type(identity)==np.ndarray)
    print(sm.toSparse(identity))
    """