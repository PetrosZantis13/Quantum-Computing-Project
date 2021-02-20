# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import SquareMatrix as sm
import numpy as np
import matplotlib.pyplot as plt
import QuantumRegister
import Presentation
    

def QFT(circuit):
    """
    Works, don't know why
    Applies quantum fourier transform to a circuit.

    Parameters
    ----------
    circuit : QuantumCircuit
        The quantum circuit to apply the QFT to

    Returns
    -------
    circuit : QuantumCircuit
        The same quantum circuit with the QFT applied to it

    """
    n = len(circuit.register.Qbits)
    
    def qft_rotations(circuit, n):
        if n==0: return circuit
        n -= 1
        circuit.addGate('h', [n])
        for qbit in range(n):
            circuit.addBigGate(('cp', qbit, n, np.pi/2**(n-qbit)))
        qft_rotations(circuit, n)
    
    def swap_registers(circuit, n):
        for qbit in range(n//2):
            circuit.addBigGate(('swap', qbit, n-qbit-1))
        return circuit
    
    def qft(circuit, n):
        qft_rotations(circuit, n)
        swap_registers(circuit, n)
        return circuit
    
    qft(circuit, n)
    
def qft_dagger(circuit):
    n = len(circuit.register.Qbits)
    
    #swap qbits
    for qbit in range(n//2):
        circuit.swap(qbit, n-qbit-1)
    for j in range(n):
        for m in range(j):
            circuit.cp(m, j, -np.pi/float(2**(j-m)))
        circuit.addGate('h', [j])
    return circuit
    
def Shor():
    """
    Doesn't work, don't know what to do next

    Returns
    -------
    None.

    """
    n_count = 8
    a = 7
    
    # Create QuantumCircuit with n_count counting qubits
    # plus 4 qubits for U to act on
    qc = QuantumCircuit.QuantumCircuit(n_count + 4)

    # Initialise counting qubits
    # in state |+>
    for q in range(n_count):
        qc.addGate('h', [q])
    
    qc.addGate('x', [3+n_count])
    

if __name__ == '__main__':
    print('Grover Circuit example:')
    Presentation.Grover_Circuit(3, [4])
    print('Bernstein-Vazirani Algorithm Example:')
    Presentation.Ber_Vaz(3, '011')
    print('QFT example:')
    Presentation.qft_example()
    """
    circuit = QuantumCircuit.QuantumCircuit(3)
    circuit.setStateVector(np.array([2,2,4,4,4,4,2,2]))
    print(circuit.register)
    print(circuit.register.Statevec)
    """
    