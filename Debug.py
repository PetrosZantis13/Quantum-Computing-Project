# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:44:25 2021

@author: mikva
"""
import QuantumCircuit
import SquareMatrix as sm
import numpy as np
import matplotlib.pyplot as plt

def diffuser(circuit):
    n_qubits = len(circuit.register.Qbits)
    
    # Apply h gates to all qubits
    for qbit in range(n_qubits):
        circuit.addGate('h', [qbit])
    # Apply x gates to all qubits
    for qbit in range(n_qubits):
        circuit.addGate('x', [qbit])
    
    circuit.ncz([i for i in range(n_qubits)])
    
    # Apply x gates to all qubits
    for qbit in range(n_qubits):
        circuit.addGate('x', [qbit])
    
    # Apply h gates to all qubits
    for qbit in range(n_qubits):
        circuit.addGate('h', [qbit])
    

def Grover_Circuit(n_qubits, measured_bits):
    """
    Returns a circuit representing Grover's algorithm for a given number of qubits and
    bits that we are interested in

    Parameters
    ----------
    n_qubits : int
        Number of qubits in the circuit.
    measured_bits : list
        list of bits that we are interested in and want to increase the amplitude of.

    Returns
    -------
    None.
    """
    grover_circuit = QuantumCircuit.QuantumCircuit(n_qubits)
    grover_circuit.addGate('h', [i for i in range(n_qubits)])
    repetitions = n_qubits - len(measured_bits) + 2
    
    grover_circuit.addmeasure()
    # calculate oracle
    elements = []
    for i in range(2**n_qubits):
        if i in measured_bits:
            elements.append((i,i,-1))
        else: elements.append((i,i,1))
    oracle_gate = sm.SparseMatrix(2**n_qubits, elements)
    
    #Add Oracle
    grover_circuit.addCustom(0, n_qubits-1, oracle_gate, 'oracle')
    
    #Add diffuser
    diffuser(grover_circuit)

    grover_circuit.addmeasure()
    # Repeat if necessary
    for i in range(repetitions):
        # Add Oracle
        grover_circuit.addCustom(0, n_qubits-1, oracle_gate, 'oracle')
        #Add diffuser
        diffuser(grover_circuit)
        grover_circuit.addmeasure()

    #show results
    results = grover_circuit.simulate(return_full=True)
    print(results[0])
    
    figure, axis = plt.subplots(1, len(results[2][1]))
    for j in range(len(results[2][1])):
        axis[j].bar([i for i in range(results[2][1][j].size)], results[2][1][j]*np.conj(results[2][1][j]))
        axis[j].set_ylim([-1,1])
        print((results[2][1][j]*np.conj(results[2][1][j])).sum())
    
    plt.show()
    
    
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

def Ber_Vaz(n, s):
    bv_circ = QuantumCircuit.QuantumCircuit(n+1)
    
    # Put ancilla in state |->
    bv_circ.addGate('h', [n])
    bv_circ.addGate('z', [n])
    
    # Apply hadamard gates before querying the oracle
    bv_circ.addGate('h', [i for i in range(n)])
    
    #Apply the inner product oracle
    s = s[::-1] # reverse s to match qubit ordering
    for q in range(n):
        if s[q] == '1': bv_circ.addBigGate(('cn', q, n))
        
    # Apply Hadamard after the oracle
    bv_circ.addGate('h', [i for i in range(n)])
    
    bv_circ.show()
    
    #must get rid of the fourth qubit in the register and measure it that way.
    
def qft_example():
    circuit = QuantumCircuit.QuantumCircuit(4)
    circuit.addGate('x', [2,1])
    circuit.addGate('h', [0,3])
    circuit.addBigGate(('cn', 0, 2))
    circuit.addmeasure()
    QFT(circuit)
    circuit.addmeasure()
    qft_dagger(circuit)
    circuit.addmeasure()
    results = circuit.simulate(return_full=True)
    
    for i, measurement in enumerate(results[2][1]):
        print(f'Measurement {i}')
        print(measurement)
        
    figure, axis = plt.subplots(1, len(results[2][1]))
    for j in range(len(results[2][1])):
        axis[j].bar([i for i in range(results[2][1][j].size)], results[2][1][j])
        axis[j].set_ylim([-1,1])
        print((results[2][1][j]*np.conj(results[2][1][j])).sum())
    

if __name__ == '__main__':
    #Grover_Circuit(3, [4])
    #Ber_Vaz(3, '011')
    qft_example()
    """
    circuit = QuantumCircuit.QuantumCircuit(3)
    circuit.setStateVector(np.array([2,2,4,4,4,4,2,2]))
    print(circuit.register)
    print(circuit.register.Statevec)
    """
    