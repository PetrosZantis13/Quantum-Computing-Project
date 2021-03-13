# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:30:35 2021

@author: mikva
"""
from QuantumCircuit import *
import Presentation
from Circuit import *
import numpy as np
import matplotlib.pyplot as plt
import time
import Sparse

def timeBenchmarks():
    max_qubits = 9
    times = np.zeros((2,max_qubits))
    for i in range(2,max_qubits):
        t1 = time.time()
        Presentation.Grover_Circuit(i, [3])
        t2 = time.time()
        times[0,i] = t2-t1
        
        t1 = time.time()
        Presentation.LazyGroverDemo(i, [3])
        t2 = time.time()
        times[1,i] = t2-t1
        
    plt.scatter([i for i in range(2,times[0].size+2)], times[0], label='sparse')
    plt.scatter([i for i in range(2,times[0].size+2)], times[1], label='lazy')
    plt.title("Runtime of Grover's Algorithm Compared to Number of Qubits")
    plt.xlabel("Number of Qubits")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()
    
def tensorTest():
    v1 = Sparse.Vector(np.array([1,0]))
    result = Sparse.Vector(np.array([1,0]))
    t1 = time.time()
    for i in range(6):
        result = result.outer(v1)
    t2 = time.time()
    print(t2-t1)
    print(result)
    pass

def compareProbabilities():
    lazy_max_measures = []
    # 2-9 qubits
    measured_bits = 1
    for n_qubits in range(2,6):
        lazy_max_measures.append([])
        grover_circuit = QuantumCircuit.QuantumCircuit('Grover', n_qubits)
        repetitions = int(np.pi/4*np.sqrt(2**n_qubits)) - 1
        grover_circuit.addGate('h', [i for i in range(n_qubits)])
        grover_circuit.addmeasure()
        # calculate oracle
        oracle = Sparse.ColMatrix(2**n_qubits)
        for i in range(2**n_qubits):
            if i in [measured_bits]:
                oracle[i,i] = -1
            else: oracle[i,i] = 1

        #Add Oracle
        grover_circuit.addCustom(0, n_qubits-1, oracle, 'oracle')
        #Add diffuser
        Presentation.diffuser(grover_circuit)
    
        grover_circuit.addmeasure()
        # Repeat if necessary
        for i in range(repetitions):
            # Add Oracle
            grover_circuit.addCustom(0, n_qubits-1, oracle, 'oracle')
            #Add diffuser
            Presentation.diffuser(grover_circuit)
            grover_circuit.addmeasure()
    
    
        #show results
        final_statevec, measurements = grover_circuit.lazysim()
        for m in measurements[1]:
           lazy_max_measures[n_qubits-2].append(max(m*m.conj()))
    print(np.array(lazy_max_measures, dtype=object))
    
if __name__ == '__main__':
    #timeBenchmarks()
    #compareProbabilities()
    tensorTest()
    pass
    