# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import numpy as np
import QuantumRegister
import Presentation
import sparse
import time
import matplotlib.pyplot as plt
        

if __name__ == '__main__':
    
    print('Grover Circuit example:')
    Presentation.Grover_Circuit(4, [3,5])
    
    
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
    
    print('Bernstein-Vazirani Algorithm Example:')
    Presentation.Ber_Vaz('1011')
    print('QFT example:')
    Presentation.qft_example()
    