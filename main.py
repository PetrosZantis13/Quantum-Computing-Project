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
    
    qbits = np.arange(2,9,1)   # mihaly's limit is 8 qubits, mine is 12
    times = np.zeros((3,len(qbits)))
    
    for q in qbits:
        
        t1 = time.time()           
        Presentation.Grover_Circuit(q, [3])
        t2 = time.time()
        times[0,q-2] = t2-t1
         
        t1 = time.time()
        Presentation.LazyGroverDemo(q, [3])
        t2 = time.time()
        times[1,q-2] = t2-t1
        
        t1 = time.time()
        g = Grover()
        g.run_circuit(q,1,'m')        
        t2 = time.time()
        times[2,q-2] = t2-t1
        
    plt.scatter(qbits, times[0], label='sparse')
    plt.scatter(qbits, times[1], label='lazy')
    plt.scatter(qbits, times[2], label='numpy')
    plt.title("Runtime of Grover's Algorithm over Number of Qubits in the system")
    plt.xlabel("Number of Qubits")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()
    
def tensorTest():
    
    loops = 15
    
    v1 = Sparse.Vector(np.array([1,0]))
    result = Sparse.Vector(np.array([1,0]))
    t1 = time.time()
    for i in range(loops):
        result = result.outer(v1)
    t2 = time.time()
    print(t2-t1)
    print(result)
    
    t1 = time.time()
    qbit_zero = Qubit(1,0)
    reg = []
    for i in range(loops):
        reg.append(qbit_zero)
    
    register = Tensor(reg)
    state = register.to_state()
    t2 = time.time()
    print(t2-t1)

def compareProbabilities():
    lazy_max_measures = []
    numpy_max_measures = []
    # 2-9 qubits
    measured_bits = 1
    for n_qubits in range(2,9):
        lazy_max_measures.append([])
        grover_circuit = QuantumCircuit('Grover', n_qubits)
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
        
        g = Grover()    
        iter, success, desired_amps = g.run_circuit(n_qubits, 1,'testing')
        numpy_max_measures.append(desired_amps)
        
    print(np.array(lazy_max_measures, dtype=object))
    print()
    print(np.array(numpy_max_measures, dtype=object))   
    
    
if __name__ == '__main__':
    
    tensorTest()
    #timeBenchmarks()
    #compareProbabilities()
    
    pass
    