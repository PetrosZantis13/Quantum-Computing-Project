"""
This module simulates a circuit with all of the Lazy Matrix implementations 
"""
import numpy as np
import Sparse

class Simulator():
    def __init__(self, gates, register, custom, measurements):
        """
        Initialiser for the simulator.

        :param gates: (list of lists) The gates representing the Quantum Circuit.
        :param register: (QuantumRegister) The quantum register representing the Quantum Circuit.
        :param custom: (dict) Dictionary of user defined custom gates.
        :param measurements: (list) The list of all places a measurement must be taken.
        """
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
        self.size = 2**self.register.Qbits.size
        self.__initialise_big_gates()
        
    def __initialise_big_gates(self):
        """
        Creates the ColMatrix representation of the larger quantum gates
        can be optimised in the future by only calling it once required
        """
        cnot = Sparse.ColMatrix(4)
        cnot[0,0] = 1
        cnot[1,3] = 1
        cnot[3,1] = 1
        cnot[2,2] = 1
        
        cz = Sparse.ColMatrix(4)
        cz[0,0] = 1
        cz[1,1] = 1
        cz[2,2] = 1
        cz[3,3] = -1
        
        cy = Sparse.ColMatrix(4)
        cy[0,0] = 1
        cy[1,1] = 1
        cy[2,3] = 1j
        cy[3,1] = -1j
        
        ccx = Sparse.ColMatrix(8)
        for i in range(6):
            ccx[i,i] = 1
        ccx[6,7] = 1
        ccx[7,6] = 1
        
        swap = Sparse.ColMatrix(4)
        swap[0,0] = 1
        swap[2,1] = 1
        swap[1,2] = 1
        swap[3,3] = 1
        
        self.large_gates = {'cn':cnot, 'cz':cz, 'ccx':ccx, 'swap':swap}
        
    def simulate(self):
        """
        Simulates the quantum circuit by iterating through all of the gates and applyig them one by one.
        Slower for smaller circuit, but better for larger ones, especially with dense matrices.

        :return self.register: (QuantumRegister) The quantum register representing the system
        :return self.measurements: (2xn list of lists) Any measurements taken during the simulation
        """
        self.gates = np.array(self.gates, dtype=object).T
        for i, row in enumerate(self.gates):
            for j, g in enumerate(row):
                if type(g)==tuple:
                    self.__addBigGate(g, j)
                elif g == 's' or g == 'i': continue
                else:
                    gate = Sparse.Gate(self.size, Sparse.toColMat(self.singlegates[g]), [j])
                    self.register.Statevec = gate.apply(self.register.Statevec)
            if i in self.measurements[0]:
                self.measurements[1].append(self.register.Statevec.Elements)
        return self.register, self.measurements
    
    def __addBigGate(self, gate_info, *args):
        """
        Helper function to clean up simulate()
        Calls the required function to apply larger or special gates

        :param gate_info: (tuple) information of multi-qubit gate
        :param *args: 
        """
        if gate_info[0]=='r':
            self.__Rt(complex(gate_info[1]), args[0])
        elif gate_info[0]=='cn':
            self.__cNot(gate_info[1:])
        elif gate_info[0]=='ccn':
            self.__ccNot(gate_info[1:])
        elif gate_info[0]=='swap':
            self.__Swap(gate_info[1:])
        elif gate_info[0]=='cz':
            self.__cZ(gate_info[1:])
        elif gate_info[0]=='cp':
            self.__cP(gate_info[1:])
        elif gate_info[0]=='ncp':
            self.__NCP(gate_info[1:])
        elif gate_info[0]=='ncz':
            self.__NCZ(gate_info[1:])
        elif gate_info[0]=='custom':
            self.__custom(gate_info[1:])
        
    
    def __cNot(self, gate_info):
        """
        Creates and applies the matrix representing the controlled x operation on 2 qubits.

        :param gate_info: (tuple(int, int, int)) First int is the control qubit, last int is the controlled qubit.
        """
        gate = Sparse.Gate(self.size, self.large_gates['cn'], list(gate_info))
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __ccNot(self, gate_info):
        """
        Creates and applies the matrix representing the controlled controlled x operation on 3 qubits.

        :param gate_info: (tuple(int, int, int)) First two ints are the control qubits, last int is the controlled qubit.
        """
        gate = Sparse.Gate(self.size, self.large_gates['ccx'], list(gate_info)[::-1])
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __cZ(self, gate_info):
        """
        Creates and applies the matrix representing the controlled z operation on two qubits.

        :param gate_info: (tuple(int, int)) The qubits the controlled z flip applies to.
        """
        gate = Sparse.Gate(self.size, self.large_gates['cz'], list(gate_info))
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __NCZ(self, gate_info):
        """
        Creates and applies the matrix representing the n controlled z operation on n qubits.

        :param gate_info: (tuple(int,..., int)) The qubits the z flip applies to.
        """
        length = max(gate_info)-min(gate_info) + 1
        ncz = Sparse.ColMatrix(2**(length))
        for i in range(2**(length)):
            ncz[i,i] = 1
        ncz[2**length-1, 2**length-1] = -1
        gate = Sparse.Gate(self.size, ncz, list(gate_info))
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __Rt(self, theta, pos):
        """
        Creates and applies the matrix representing the rotation gate on one qubit.

        :param theta: (float) Rotation angle.
        :param pos: (int) position of the qubit.
        """
        mat = np.array([[1,0], [0, np.exp(1j*theta)]])
        gate = Sparse.Gate(self.size, Sparse.toColMat(mat), [pos])
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __Swap(self, gate_info):
        """
        Creates and applies the matrix representing the swap operation between two qubits.

        :param gate_info: (tuple(int, int)) The two gates to be swapped.
        """
        gate = Sparse.Gate(self.size, self.large_gates['swap'], list(gate_info))
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __cP(self, gate_info):
        mat = Sparse.ColMatrix(4)
        mat[0,0] = 1
        mat[1,1] = 1
        mat[2,2] = 1
        mat[3,3] = np.exp(1j*gate_info[-1])
        gate = Sparse.Gate(self.size, mat, list(gate_info)[:-1])
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __NCP(self, gate_info):
        """
        Creates and applies the matrix representing the n controlled phase operation on n qubits.

        :param gate_info: (tuple(int,..., int, float)) The qubits the rotation applies to, Float for the rotation angle.
        """
        length = max(gate_info)-min(gate_info) + 1
        ncp = Sparse.ColMatrix(2**(length))
        for i in range(2**(length)):
            ncp[i,i] = 1
        ncp[2**length-1, 2**length-1] = np.exp(gate_info[-1])
        gate = Sparse.Gate(self.size, ncp, list(gate_info)[:-1])
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)
    
    def __custom(self, gate_info):
        """
        Creates and applies a custom, user defined matrix to the system
        
        :param gate_info: (tuple(int, int, str)) The ints represent the range of qubits the gate applies to, the string is the name of the gate.
        """
        bits = [i for i in range(min(list(gate_info)[:-1]), max(gate_info[:-1])+1)]
        gate = Sparse.Gate(self.size, self.customgates[gate_info[-1]], bits)
        self.register.Statevec = gate.apply(self.register.Statevec.Elements)