# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import QuantumRegister
import numpy as np

if __name__ == '__main__':    
    circuit = QuantumCircuit.QuantumCircuit(3)
    circuit.addGate('x', [0])
    circuit.addGate('h', [0,1])
    circuit.addGate('h', [2])
    
    print(np.array(circuit.gates, dtype = object))
    print(circuit.register)
    circuit.simulate()
    #print(circuit.makeMatrices())