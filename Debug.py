"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import numpy as np
import QuantumRegister
import Presentation
import Sparse
import time
import matplotlib.pyplot as plt
import sys
        
#Despo one love
def numpy_vs_lazy():
    min_qubits = 8
    max_qubits = 14
    had = Sparse.ColMatrix(2)
    had[0,0] = 1/np.sqrt(2)
    had[0,1] = 1/np.sqrt(2)
    had[1,0] = 1/np.sqrt(2)
    had[1,1] = -1/np.sqrt(2)
    np_had = np.array([[1,1],[1,-1]])/np.sqrt(2)
    
    times = np.zeros((2,max_qubits-min_qubits))
    memoryusage = np.zeros((2,max_qubits-min_qubits))

    for i in range(min_qubits, max_qubits):
        test_vector = np.ones(2**i)/np.sqrt(2**i)
        #test_vector[0] = 1
        t1 = time.time()
        for qubit in range(i):
            gate = Sparse.Gate(2**i, had, [qubit])
            test_vector = gate.apply(test_vector)
        t2 = time.time()
        memoryusage[0,i-min_qubits] = sys.getsizeof(gate)
        #print(test_vector)
        
        test_vector = np.ones(2**i)/np.sqrt(2**i)
        #test_vector[0] = 1
        t3 = time.time()
        gate = np.array([1])
        for qubit in range(i):
            gate = np.kron(gate, np_had)
        test_vector = gate.dot(test_vector)
        #print(test_vector)
        t4 = time.time()
        times[0,i-min_qubits] = t2-t1
        times[1,i-min_qubits] = t4-t3
        memoryusage[1,i-min_qubits] = sys.getsizeof(gate)
    
    print('Time taken to superimpose all elements of an array using hadamard gates')
    print(times)
    print(memoryusage)
    fig1 = plt.figure()
    ax1 = fig1.add_axes([0.1,0.1,0.8,0.8])
    ax1.plot([i for i in range(min_qubits, max_qubits)], times[0], label='Lazy Implementation')
    ax1.plot([i for i in range(min_qubits, max_qubits)], times[1], label='Numpy Implementation')
    fig1.suptitle("Runtime of Applying a Hadamard Gate to Every Qubit in a Register", fontsize = '15')
    plt.xlabel("Number of Qubits", fontsize = '14')
    plt.ylabel("Runtime (s)", fontsize = '14')
    plt.yscale('log')
    plt.xlim((min_qubits, max_qubits-1))
    ax1.legend()
    plt.show()

if __name__ == '__main__':
    
    #print('Grover Circuit example:')
    #Presentation.Grover_Circuit(2, [3])
    
    """
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
    """
    
    """
    t1 = time.time()
    Presentation.Grover_Circuit(5, [3])
    t2 = time.time()
    
    t3 = time.time()
    Presentation.LazyGroverDemo(5, [3])
    t4 = time.time()
    
    print(f'Time taken for sparse implementation: {t2-t1}')
    print(f'Time taken for lazy implementation: {t4-t3}')
    """
    """
    # Measuring the time it takes to apply Grover's Algorithm to circuits of different size.
    times = []
    for i in range(2,9):
        t1 = time.time()
        Presentation.Grover_Circuit(i, [3])
        t2 = time.time()
        times.append(t2-t1)
    plt.scatter([i for i in range(2,9)], times)
    plt.title("Runtime of Grover's Algorithm Compared to Number of Qubits")
    plt.xlabel("Number of Qubits")
    plt.ylabel("Runtime (s)")
    print(times)
    """
    #print('Bernstein-Vazirani Algorithm Example:')
    Presentation.Ber_Vaz('1011')
    #print('QFT example:')
    #Presentation.qft_example()
    