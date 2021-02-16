# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import QuantumRegister
import SquareMatrix as sm
import numpy as np

def Grover_Circuit():
    grover_circuit = QuantumCircuit.QuantumCircuit(2)
    grover_circuit.addGate('h', [0,1]) # Create equal probabilities for all states
    grover_circuit.addBigGate(('cz', 0, 1)) # Add oracle
    
    # Add diffuser
    grover_circuit.addGate('h', [0,1]) 
    
    # Reflection
    grover_circuit.addGate('z', [0,1])
    grover_circuit.addBigGate(('cz', 0, 1))
    
    grover_circuit.addGate('h', [0,1]) # End of diffuser
    #show results
    grover_circuit.show()
    
def QFT(circuit):
    """
    Works, don't know why'

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
        print(n)
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
    qc = QuantumCircuit(n_count + 4)

    # Initialise counting qubits
    # in state |+>
    for q in range(n_count):
        qc.addGate('h', [q])
    
    qc.addGate('x', [3+n_count])

if __name__ == '__main__':
    #Grover_Circuit()
    circuit = QuantumCircuit.QuantumCircuit(3)
    #circuit.addGate('x', [0,2])
    #circuit.cp(0,2,np.exp(np.pi/4))
    
    circuit.addGate('x', [0,2])
    circuit.addGate('h', [0,1,2])
    QFT(circuit)
    
    
    circuit.show()
    
    """
    n = 5
    QFT(circuit)
    circuit.show()
    """
    """
    circuit.r([0], n*np.pi/4)
    circuit.r([1], n*np.pi/2)
    circuit.r([2], n*np.pi)
    circuit.addGate('h', [0,1,2])
    newgates = []
    for row in circuit.gates:
        newgates.append(row[::-1])
    circuit.gates = newgates
    circuit.show()
    """