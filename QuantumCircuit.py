# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:35:20 2021

@author: mikva
"""
import QuantumRegister
import numpy as np
import SquareMatrix as sm
import Simulator

class QuantumCircuit:
    def __init__(self, size):
        """
        Initiates the quantum circuit.

        Parameters
        ----------
        reg : QuantumRegister object
            The quantum register to be made into a circuit.

        Returns
        -------
        None.
        """
        self.singlegates = {'x' : np.array([[0,1], [1,0]]),
                      'y' : np.array([[0,-1j], [1j,0]]),
                      'z' : np.array([[1,0], [0,-1]]),
                      'h' : np.array([[1,1],[1,-1]])/np.sqrt(2),
                      'p' : np.array([[1,0],[0,1j]]),
                      't' : np.array([[1,0],[0,np.exp(1j*np.pi/4)]]),
                      'i' : np.eye(2)
                      }
        self.customgates = {}
        self.register = QuantumRegister.QuantumRegister(size)
        #self.classical_register = QuantumRegister.ClassicalRegister(size)
        self.gates = []
        for i in range(self.register.Qbits.size):
            self.gates.append(['i'])
        self.gateindex = 0
        self.measurements = []
        
    def setStateVector(self, newVector):
        assert self.register.Statevec.Elements.size == len(newVector), 'Wrong dimension for new vector'
        self.register.setStateVec(newVector)
        
    def addGate(self, gate, bits):
        """
        Adds an arbitrary gate to the set of gates stored in the circuit

        Parameters
        ----------
        gate : char
            The type of gate to be added. Current options are:'x', 'y', 'z', 'h', 'p', 't'
        
        bits : array_like
            The position of bits the gate is needed to be added
            
        Returns
        -------
        None.

        """
        # Check availability
        available = True
        for i in bits: 
            if self.gates[i][self.gateindex]!='i':
                available = False
        if available:
            for i in bits:
                self.gates[i][self.gateindex] = gate
        else:
            for i in range(len(self.gates)): # Go through all rows of self.gates and add in the gate if needed, add in 'i' if not needed
                if i in bits:
                    self.gates[i].append(gate)
                else:
                    self.gates[i].append('i')
            self.gateindex += 1
        
    """
    def x(self, bits):
        self.addGate('x', bits)
    
    def y(self, bits):
        self.addGate('y', bits)
    
    #Pls someone else do the rest
    """
    def addBigGate(self, gate_info):
        """
        Adds the representation of a gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        Parameters
        ----------
        gate_info : tuple(str, int, int...)
            The gate info for the large gate in the form of string(type of gate), 
            and ints for control bits, then the controlled bit for the last int if needed

        Returns
        -------
        None.

        """
        
        if gate_info[0] == 'cp' or gate_info[0]=='ncp' or gate_info[0]=='custom':
            low_lim, high_lim = min(gate_info[1:-1]), max(gate_info[1:-1])
        else: low_lim, high_lim = min(gate_info[1:]), max(gate_info[1:])
        
        available = True
        for i in range(low_lim, high_lim+1): 
            if self.gates[i][self.gateindex]!='i':
                available = False
        if available:
            self.gates[low_lim][self.gateindex] = gate_info
            for i in range(low_lim+1, high_lim+1):
                self.gates[i][self.gateindex] = 's'
        else:
            for i in range(len(self.gates)):
                self.gates[i].append('i')
            self.gateindex += 1
            self.addBigGate(gate_info)
    
    def r(self, bits, theta):
        self.addGate(('r', theta), bits)
    
    def bitactive(self, n, bit):
        return ((n>>(bit)) & 1) == 1
    
    def toggle(self, n, bit):
        return n ^ (1 << bit)
    
    def cnot(self, qbit1, qbit2):
        """
        Adds the representation of a cnot gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        Parameters
        ----------
        qbit1 : int
            Control Qubit
        qbit2 : int
            Controlled Qubit

        Returns
        -------
        None.

        """
        self.addBigGate(('cn', qbit1, qbit2))
            
    def ccnot(self, control1, control2, qubit):
        """
        Adds the representation of a ccnot gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        Parameters
        ----------
        qbit1 : int
            Control Qubit
        qbit2 : int
            Controlled Qubit

        Returns
        -------
        None.
        """
        self.addBigGate(('ccn', control1, control2, qubit))


    def ncp(self, bits, phi):
        """
        Adds a phase gate controlled by n other qubits

        Parameters
        ----------
        bits : List if ints
            The control qubits
        phi : float
            Rotation parameter

        Returns
        -------
        None.

        """
        gate_info = ['ncp']
        gate_info += bits
        gate_info.append(phi)
        #print(gate_info)
        self.addBigGate(tuple(gate_info))
        
    def ncz(self, bits):
        gate_info = ['ncz']
        gate_info += bits
        self.addBigGate(tuple(gate_info))
        
    def addCustom(self, qbit1, qbit2, gate, name):
        assert max(qbit1, qbit2) <= len(self.gates), 'Gate too large to be added'
        assert 2**np.abs((qbit2 - qbit1)+1) == gate.Dimension, f'Dimensions of gate do not match the given qubits {2**np.abs(qbit2-qbit1)}'
        gate_info = ['custom', qbit1, qbit2, name]
        self.customgates.update({str(name) : gate})
        self.addBigGate(tuple(gate_info))
    
    def cp(self, qbit1, qbit2, phi):
        self.addBigGate(('cp', qbit1, qbit2, phi))
    
    def swap(self, qbit1, qbit2):
        self.addBigGate(('swap', qbit1, qbit2))
        
    def simulate(self, return_full=False):
        """
        Applies the circuit to the initialized statevector

        Returns
        -------
        The final state of the state vector
        Planned: any measurements throughout the experiment
        
        """
        if return_full: 
            self.register, operations, measurements = Simulator.Simulator(self.gates, self.register, self.customgates, self.measurements).simulate(return_full = True)
            return self.register, operations, measurements
        else: self.register = Simulator.Simulator(self.gates, self.register, self.customgates, self.measurements).simulate()

    def addmeasure(self):
        """
        Adds a space where a measurement should be made. Mesurements are only made when simulating the circuit.

        Returns
        -------
        None.

        """
        self.measurements.append(self.gateindex)
        for i in range(len(self.gates)):
            self.gates[i].append('i')
        self.gateindex += 1

    def show(self):
        print('Register defined as:')
        print(self.register)
        #self.register.measure()
        print('Gates are:')
        print(np.array(self.gates, dtype = object), '\n')
        
        self.simulate()
        print('Final state of the register is:')
        print(self.register)
        print('With statevector')
        print(self.register.Statevec)
        self.register.measure()
    
if __name__ == '__main__':
    pass