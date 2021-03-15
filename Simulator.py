"""
This module simulates a circuit. It also defines the necessary gates.
"""
import numpy as np
import Sparse

class Simulator():
    def __init__(self, gates, register, custom, measurements):
        self.gates = gates
        self.register = register
        self.singlegates = {'x' : np.array([[0,1], [1,0]]),
                      'y' : np.array([[0,-1j], [1j,0]]),
                      'z' : np.array([[1,0], [0,-1]]),
                      'h' : np.array([[1,1],[1,-1]])/np.sqrt(2),
                      'p' : np.array([[1,0],[0,1j]]),
                      't' : np.array([[1,0],[0,np.exp(1j*np.pi/4)]]),
                      'i' : np.eye(2)
                      }
        self.customgates = custom
        self.measurements = [measurements, []]

    def __bitactive(self, n, bit):
        """
        Checks whether a given integer has a particular bit active

        :param n: (int) Integer to check
        :param bit: (int) The position of the bit to check
        :return: (Boolean) True of bit is active, false if not
        """
        return ((n>>(bit)) & 1) == 1
        
    def __toggle(self, n, bit):
        """
        Toggles a specific bit in an integer

        :param n: (int) Integer to toggle
        :param bit: (int) The position of the bit to toggle
        :return: (int) The new integer created by toggling the bit
        """
        return n ^ (1 << bit)
    
    def __cNot(self, gate_info):
        """
        Creates an arbitrary sized controlled not gate between two arbitrary qbits.

        :param gate_info: (tuple(int, int)) Position in the circuit of the control qubit and the controlled qubit
        :return: (SparseMatrix) The cnot gate entangling the two qubits given.
        """
        qbit1, qbit2 = gate_info
            
        if qbit1>qbit2:
            control_bit = np.abs(qbit2-qbit1)
            controlled_bit = 0
        else:
            control_bit = 0
            controlled_bit = qbit2 - qbit1
            
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.__bitactive(i, control_bit):
                col = self.__toggle(i, controlled_bit)
                elements.append(Sparse.MatrixElement(i, col, 1))
            else: elements.append(Sparse.MatrixElement(i,i,1))
        return Sparse.SparseMatrix(dimension, elements)
    
    def __ccNot(self, gate_info):
        """
        Creates a Sparsematrix representing the controlled-controlled-not (ccnot or Tiffoli) 
        gate for the given qubits. Can be applied to any exisiting qubits.

        :param gate_info: (tuple(int, int, int)) first, second qubit controlling the gate and the qubit controlled by the other two
        :return: (SparseMatrix)  Matrix representation of the gate
        """
        control1, control2, qbit3 = gate_info
        # Reset the values to range from 0 to maxval
        minval = min(control1, control2, qbit3)
        maxval = max(control1, control2, qbit3) - minval
        control1 = control1 - minval
        control2 = control2 - minval
        qbit3 = qbit3 - minval
            
        # Create elements and calculate dimensions
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(maxval+1)
            
        # For each possible bit check whether the control qubits are active
        for i in range(1, dimension):
            if self.__bitactive(i, control1) and self.__bitactive(i, control2):
                # if control qubits are active, calculate the new value and insert into matrix
                col = self.__toggle(i, qbit3)
                elements.append(Sparse.MatrixElement(i, col, 1))
            else: elements.append(Sparse.MatrixElement(i,i,1))
        return Sparse.SparseMatrix(dimension, elements)
    
    def __cZ(self, gate_info):
        """
        Creates a controlled z gate given 2 qubits

        :param gate_info: (tuple(int, int)) The two gates to control the z
        :return: (SparseMatrix) Representation of the cz gate
        """
        qbit1, qbit2 = gate_info
        shift = min(qbit1, qbit2)
        qbit1 = qbit1 - shift
        qbit2 = qbit2 - shift
            
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.__bitactive(i, qbit1) and self.__bitactive(i, qbit2):
                elements.append(Sparse.MatrixElement(i, i, -1))
            else: elements.append(Sparse.MatrixElement(i,i,1))
        return Sparse.SparseMatrix(dimension, elements)
    
    def __cP(self, gate_info):
        """
        Creates a controlled phase gate for the given qubits

        :param gate_info: (tuple(int, int, float)) The information supplied to the gate. Control qubits as ints, float as the phase.
        :return: (SparseMatrix) Representation of the cp gate
        """
        qbit1, qbit2, phi = gate_info
        
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(1, dimension):
            if self.__bitactive(i, qbit1) and self.__bitactive(i, qbit2):
                elements.append(Sparse.MatrixElement(i, i, np.exp(1j*phi)))
            else: elements.append(Sparse.MatrixElement(i,i,1))
        return Sparse.SparseMatrix(dimension, elements)
        
    def __NCP(self, gate_info):
        """
        Adds a phase gate controlled by an arbitrary number of bits
    
        :param gate_info: (tuple(int, int, int..., float)) Control qubits as ints, phase as a float.
        :return: (SparseMatrix) Matrix representation of gate.
        """
        bits = np.array(gate_info[:-1])
        bits = bits - min(bits)
        phi = gate_info[-1]
        
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(max(bits)-min(bits)+1)
        for i in range(1, dimension):
            active = True
            for bit in bits:
                if not self.__bitactive(i, bit):
                    active = False
                    break
            if active: elements.append(Sparse.MatrixElement(i, i, np.exp(1j*phi)))
            else: elements.append(Sparse.MatrixElement(i, i, 1))
        return Sparse.SparseMatrix(dimension, elements)
    
    def __NCZ(self, gate_info):
        """
        Adds a z gate controlled by an arbitrary number of bits
    
        :param gate_info: (tuple(int, int, int...,)) Control qubits as ints, arbitrary number
        :return: (SparseMatrix) Matrix representatin of the gate
        """
        bits = np.array(gate_info)
        bits = bits - min(bits)
        
        elements = [Sparse.MatrixElement(0,0,1)]
        dimension = 2**(max(bits)-min(bits)+1)
        for i in range(1, dimension):
            active = True
            for bit in bits:
                if not self.__bitactive(i, bit):
                    active = False
                    break
            if active: elements.append(Sparse.MatrixElement(i, i, -1))
            else: elements.append(Sparse.MatrixElement(i, i, 1))
        return Sparse.SparseMatrix(dimension, elements)
    
    def __Swap(self, gate_info):
        """
        Creates the matrix representing the swap operation between two qubits.

        :param gate_info: (tuple(int, int)) The two gates to be swapped.
        :return: (SparseMatrix) Matrix representation of the swap gate.
        """
        qbit1, qbit2 = gate_info
        shift = min(qbit1, qbit2)
        qbit1 = qbit1 - shift
        qbit2 = qbit2 - shift
        elements = []
        dimension = 2**(np.abs(qbit2-qbit1)+1)
        for i in range(0, dimension):
            col = i
            if (self.__bitactive(i, qbit1) and not self.__bitactive(i, qbit2)) or (not self.__bitactive(i, qbit1) and self.__bitactive(i, qbit2)):
                col = self.__toggle(self.__toggle(i, qbit1), qbit2)
            elements.append(Sparse.MatrixElement(i, col, 1))
            
        return Sparse.SparseMatrix(dimension, elements)
    
    def __addLargeGate(self, gate_info):
        """
        Helper function for makeMatrices(). Calls the creators for the larger gates based
        info provided.

        :param gate_info: (tuple) information of multi-qubit gate
        :return: (SparseMatrix) Matrix representation of the operation for the gates given.
        """
        #print(gate_info)
        if gate_info[0]=='r':
            operation = self.__Rt(complex(gate_info[1]))
        elif gate_info[0]=='cn':
            operation = self.__cNot(gate_info[1:])
        elif gate_info[0]=='ccn':
            operation = self.__ccNot(gate_info[1:])
        elif gate_info[0]=='swap':
            operation = self.__Swap(gate_info[1:])
        elif gate_info[0]=='cz':
            operation = self.__cZ(gate_info[1:])
        elif gate_info[0]=='cp':
            operation = self.__cP(gate_info[1:])
        elif gate_info[0]=='ncp':
            operation = self.__NCP(gate_info[1:])
        elif gate_info[0]=='ncz':
            operation = self.__NCZ(gate_info[1:])
        elif gate_info[0]=='custom':
            operation = self.customgates[gate_info[-1]]
        
        return operation
        
    def makeMatrices(self):
        """
        Creates the matrices that will be applied to the wavevector
    
        :return: (array) list of np matrices that will be applied to the statevector
        """
        # We should make Sparse matrix representations of single gates from the beginning.
        gates = np.array(self.gates, dtype = object).T
        #debug
        #print('Gates are:')
        #print(gates)
            
        bigmats = []
        for i, slot in enumerate(gates):
            bigmat = Sparse.SparseMatrix(1, [Sparse.MatrixElement(0,0,1)])
            for j in slot:
                if type(j)==tuple:
                    bigmat = self.__addLargeGate(j).tensorProduct(bigmat)
                elif j == 's': continue
                else: 
                    bigmat = Sparse.makeSparse(self.singlegates[j]).tensorProduct(bigmat)
            bigmats.append(bigmat)
            
        return np.array(bigmats)
        
    def __Rt(self, theta):
        """
        Creates an r gate with the given phase
    
        :param theta: (float) The angle in radians which the qubit should be rotated by.
        :return: (SparseMatrix) Matrix representation of the r gate.
        """
        return Sparse.makeSparse(np.array([[1, 0], [0, np.exp(1j*theta)]], dtype=complex))
    
    def simulate(self, return_full = False):
        """
        Applies the circuit to the initialized statevector

        :param return_full: (Boolean) True if operations and measurements need to be returned.
        :return: The register, if return_full: the register, operations and any measurements.
        """
        operations = self.makeMatrices()
        for i, operation in enumerate(operations):
            #print(i)
            #print(operation)
            self.register.Statevec = operation.apply(self.register.Statevec)
            if i in self.measurements[0]:
                self.measurements[1].append(self.register.Statevec.Elements)
            
        if return_full: return self.register, operations, self.measurements
        return self.register
    
    def simulate2(self):
        """
        Applies the circuit to the initialized statevector without storing the operations

        :return: The register and any measurements made
        """
        gates = np.array(self.gates, dtype = object).T
        #debug
        #print('Gates are:')
        #print(gates)
        
        for i, slot in enumerate(gates):
            bigmat = Sparse.SparseMatrix(1, [Sparse.MatrixElement(0,0,1)])
            for j in slot:
                if type(j)==tuple:
                    bigmat = self.__addLargeGate(j).tensorProduct(bigmat)
                elif j == 's': continue
                else: 
                    bigmat = Sparse.makeSparse(self.singlegates[j]).tensorProduct(bigmat)
            self.register.Statevec = bigmat.apply(self.register.Statevec)
            if i in self.measurements[0]:
                self.measurements[1].append(self.register.Statevec.Elements)
        
        return self.register, self.measurements