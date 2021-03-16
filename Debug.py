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
        

if __name__ == '__main__':
    
    #print('Grover Circuit example:')
    #Presentation.Grover_Circuit(4, [3,5])
    
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
    #Presentation.Ber_Vaz('1011')
    #print('QFT example:')
    #Presentation.qft_example()
    