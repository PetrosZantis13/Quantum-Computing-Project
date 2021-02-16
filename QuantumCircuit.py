# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:35:20 2021

@author: mikva
"""
import QuantumRegister
import numpy as np
import SquareMatrix as sm

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
        self.register = QuantumRegister.QuantumRegister(size)
        #self.classical_register = QuantumRegister.ClassicalRegister(size)
        self.gates = []
        for i in range(self.register.Qbits.size):
            self.gates.append(['i'])
        self.gateindex = 0
        
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
        low_lim, high_lim = min(gate_info[1:]), max(gate_info[1:])
        if gate_info[0] == 'cp':
            low_lim, high_lim = min(gate_info[1:-1]), max(gate_info[1:-1])
            print(low_lim, high_lim)
        
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
    
    def cNot(self, gate_info):
        """
        Creates an arbitrary sized controlled not gate between two arbitrary qbits.

        Parameters
        ----------
        qbit1 : int
            Position in the circuit of the control qubit
        qbit2 : int
            Position in the circuit of the controlled qubit

        Returns
        -------
        SparseMatrix
            The cnot gate entangling the two qubits given.
        """
        qbit1, qbit2 = gate_info
        
        if qbit1>qbit2:
            control_bit = np.abs(qbit2-qbit1)
            controlled_bit = 0
        else:
            control_bit = 0
            controlled_bit = qbit2 - qbit1
        
        elements = [(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.bitactive(i, control_bit):
                col = self.toggle(i, controlled_bit)
                elements.append((i, col, 1))
            else: elements.append((i,i,1))
        return sm.SparseMatrix(dimension, elements)
    
    def ccNot(self, gate_info):
        """
        Creates a sparsematrix representing the controlled-controlled-not (ccnot or Tiffoli) 
        gate for the given qubits. Can be applied to any exisiting qubits.

        Parameters
        ----------
        control1 : int
            first qubit controlling the gate
        control2 : int
            second qubit controlling the gate
        qbit3 : int
            The qubit to be controlled by the other two

        Returns
        -------
        SparseMatrix
            Matrix representation of the gate

        """
        control1, control2, qbit3 = gate_info
        # Reset the values to range from 0 to maxval
        minval = min(control1, control2, qbit3)
        maxval = max(control1, control2, qbit3) - minval
        control1 = control1 - minval
        control2 = control2 - minval
        qbit3 = qbit3 - minval
        
        # Create elements and calculate dimensions
        elements = [(0,0,1)]
        dimension = 2**(maxval+1)
        
        # For each possible bit check whether the control qubits are active
        for i in range(1, dimension):
            if self.bitactive(i, control1) and self.bitactive(i, control2):
                # if control qubits are active, calculate the new value and insert into matrix
                col = self.toggle(i, qbit3)
                elements.append((i, col, 1))
            else: elements.append((i,i,1))
        return sm.SparseMatrix(dimension, elements)
    
    def cZ(self, gate_info):
        """
        Creates a controlled z gate given 2 qubits

        Parameters
        ----------
        gate_info : tuple(int, int)
            The two gates to control the z

        Returns
        -------
        SparseMatrix
            Representation of the cz gate
        """
        qbit1, qbit2 = gate_info
        
        elements = [(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.bitactive(i, qbit1) and self.bitactive(i, qbit2):
                elements.append((i, i, -1))
            else: elements.append((i,i,1))
        return sm.SparseMatrix(dimension, elements)
    
    def cP(self, gate_info):
        """
        Creates a controlled phase gate for the given qubits

        Parameters
        ----------
        gate_info : tuple(int, int, float)
            The information supplied to the gate. Control qubits as ints, float as the phase.

        Returns
        -------
        SparseMatrix
            Representation of the cp gate

        """
        qbit1, qbit2, phi = gate_info
        
        elements = [(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.bitactive(i, qbit1) and self.bitactive(i, qbit2):
                elements.append((i, i, np.exp(1j*phi)))
            else: elements.append((i,i,1))
        return sm.SparseMatrix(dimension, elements)
    
    def cp(self, qbit1, qbit2, phi):
        self.addBigGate(('cp', qbit1, qbit2, phi))
    
    def swap(self, qbit1, qbit2):
        self.addBigGate(('swap', qbit1, qbit2))
    
    def Swap(self, gate_info):
        qbit1, qbit2 = gate_info
        qbit1 = qbit1 - min(qbit1, qbit2)
        qbit2 = qbit2 - min(qbit1, qbit2)
        elements = []
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(0, dimension):
            col = i
            if (self.bitactive(i, qbit1) and not self.bitactive(i, qbit2)) or (not self.bitactive(i, qbit1) and self.bitactive(i, qbit2)):
                col = self.toggle(self.toggle(i, qbit1), qbit2)
            elements.append((i, col, 1))
        return sm.SparseMatrix(dimension, elements)
    
    def addLargeGate(self, gate_info):
        """
        Helper function for makeMatrices(). Calls the creators for the larger gates based
        info provided.

        Parameters
        ----------
        gate_info : tuple
            information concerning the gate

        Returns
        -------
        operation : SparseMatrix
            MAtrix representation of the operation for the gates given.

        """
        if gate_info[0]=='r':
            operation = self.Rt(complex(gate_info[1]))
        elif gate_info[0]=='cn':
            operation = self.cNot(gate_info[1:])
        elif gate_info[0]=='ccn':
            operation = self.ccNot(gate_info[1:])
        elif gate_info[0]=='swap':
            operation = self.Swap(gate_info[1:])
        elif gate_info[0]=='cz':
            operation = self.cZ(gate_info[1:])
        elif gate_info[0]=='cp':
            operation = self.cP(gate_info[1:])
        
        return operation
    
    def makeMatrices(self):
        # We should make sparse matrix representations of single gates from the beginning.
        """
        Creates the matrices that will be applied to the wavevector

        Returns
        -------
        bigmats : numpy array
            list of np matrices that will be applied to the statevector

        """
        gates = np.array(self.gates, dtype = object).T
        #debug
        print('Gates are:')
        print(gates)
        
        bigmats = []
        for i, slot in enumerate(gates):
            bigmat = sm.SparseMatrix(1, [(0,0,1)])
            for j in slot:
                if type(j)==tuple:
                    bigmat = self.addLargeGate(j).tensorProd(bigmat)
                elif j == 's': continue
                else: bigmat = sm.toSparse(self.singlegates[j]).tensorProd(bigmat)
            bigmats.append(bigmat)
        
        
        return np.array(bigmats)
    
    def Rt(self, theta):
        """
        Creates an r gate with the given phase

        Parameters
        ----------
        theta : float
            The angle in radians which the qubit should be rotated by.

        Returns
        -------
        SparseMatrix
            Matrix representation of the r gate.

        """
        return sm.toSparse(np.array([[1, 0], [0, np.exp(1j*theta)]], dtype=complex))
        
    def simulate(self):
        """
        Applies the circuit to the initialized statevector

        Returns
        -------
        The final state of the state vector
        Planned: any measurements throughout the experiment
        
        """
        operations = self.makeMatrices()
        for operation in operations:
            self.register.Statevec = operation.Apply(self.register.Statevec)
            print('Current operation:')
            print(operation.toDense())
            
            print('Current statevector is:')
            print(self.register)
            print('With statevector')
            print(self.register.Statevec)
        
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
        #self.register.measure()
        
    
if __name__ == '__main__':
    circuit = QuantumCircuit(3)
    #print(circuit.ccNot(2,0,1).toDense())
    circuit.r([0], 5*np.pi/2)
    circuit.show()
    circuit.swap(0,2)
    """
    for i, bit in enumerate(circuit.register.Qbits):
        print(i, bit)
    circuit.show()
    for i, bit in enumerate(circuit.register.Qbits):
        print(i, bit)
    """