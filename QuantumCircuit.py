"""
This modules creates a Circuit for with the specified gates by the User. The User can also create their own gate in this module.
"""
import QuantumRegister
import numpy as np
import Simulator
from Interface import Interface

class QuantumCircuit(Interface):
    def __init__(self, name, size):
        """
        Initiates the quantum circuit.

        :param name: (string) The name of the Quantum Circuit
        
        :param size: (int) The nuber of qubits in the Quantum Circuit

        """
        super().__init__(name)
        self.size = size
        self.customgates = {}
        self.register = QuantumRegister.QuantumRegister(size)
        #self.classical_register = QuantumRegister.ClassicalRegister(size)
        self.gates = []
        for i in range(self.register.Qbits.size):
            self.gates.append(['i'])
        self.gateindex = 0
        self.measurements = []
        self.final_measurements = None
        
    def setStateVector(self, newVector):
        """
        Allows the user to define the state vector for the quantum circuit

        :param newVector: (list) The vector that the user wants as the new state vector
        """
        assert self.register.Statevec.Elements.size == np.array(newVector).size, 'Wrong dimension for new vector'
        self.register.setStateVec(newVector)
        
    def addGate(self, gate, bits):
        """
        Adds an arbitrary gate to the set of gates stored in the circuit

        :param gate: (char) The type of gate to be added. Current options are:'x', 'y', 'z', 'h', 'p', 't'
        
        :param bits: (list) The position of bits the gate is needed to be added

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
        
    def addBigGate(self, gate_info):
        """
        Adds the representation of a gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        :param gate_info: (tuple) The gate info for the large gate in the form of string(type of gate), and ints for control bits, then the controlled bit for the last int if needed.

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
        """
        Adds a rotation matrix to the circuit

        :param bits: (list) The qubits that the matrices will be applied to
        :param theta: (float) Rotation angle

        """
        self.addGate(('r', theta), bits)
    
    def cnot(self, qbit1, qbit2):
        """
        Adds the representation of a cnot gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        :param qbit1: (int) Control Qubit
        :param qbit2: (int) Controlled Qubit

        """
        self.addBigGate(('cn', qbit1, qbit2))
            
    def ccnot(self, control1, control2, qubit):
        """
        Adds the representation of a ccnot gate into self.gates.
        The gate will be iplemented later on when the circuit is simulated.

        :param qbit1: (int) Control Qubit
        :param qbit2: (int) Controlled Qubit
        """
        self.addBigGate(('ccn', control1, control2, qubit))

    def ncp(self, bits, phi):
        """
        Adds a phase gate controlled by n other qubits

        :param bits: (list) The control qubits
        :param phi: (float) Rotation parameter

        """
        gate_info = ['ncp']
        gate_info += bits
        gate_info.append(phi)
        #print(gate_info)
        self.addBigGate(tuple(gate_info))
        
    def ncz(self, bits):
        """
        Adds the representation of an n controlled z gate to the circuit

        :param bits: (list) The control bits for the gate

        """
        gate_info = ['ncz']
        gate_info += bits
        self.addBigGate(tuple(gate_info))
        
    def addCustom(self, qbit1, qbit2, gate, name):
        """
        Adds a custom, user defined gate to the circuit. Does not check for unitary matrices, 
        so have to be careful when using it. The dimension of the gate must match the dimension
        allowed by the affected qubits.

        :param qbit1: (int) Position of the qubit with the smaller index.
        :param qbit2: (int) Position of the qubit with the higher index.
        :param gate: (SparseMatrix) SparseMAtrix representation of the gate to be added to the circuit.
        :param name: (str) The name of the custom gate.

        """
        assert max(qbit1, qbit2) <= len(self.gates), 'Gates not in the circuit'
        assert 2**np.abs((qbit2 - qbit1)+1) == gate.Dimension, f'Dimensions of gate do not match the given qubits {2**np.abs(qbit2-qbit1)}'
        gate_info = ['custom', qbit1, qbit2, name]
        self.customgates.update({str(name) : gate})
        self.addBigGate(tuple(gate_info))
    
    def cp(self, qbit1, qbit2, phi):
        """
        Adds the representation of a controlled phase gate to the circuit.

        :param qbit1: (int) Control bit 1
        :param qbit2: (int) Control bit 2
        :param phi: (float) Rotation angle

        """
        self.addBigGate(('cp', qbit1, qbit2, phi))
    
    def swap(self, qbit1, qbit2):
        """
        Adds the representation of a swap gate to the circuit.

        :param qbit1: (int) qubit to be swapped
        :param qbit2: (int) qubit to be swapped

        """
        self.addBigGate(('swap', qbit1, qbit2))
        
    def run_circuit(self, return_full=False):
        """
        Applies the circuit to the initialized state vector

        :return: The final state of the state vector. If return_full: returns all operations along with the statevector and measurements
        
        """
        if return_full: 
            self.register, operations, self.final_measurements = Simulator.Simulator(self.gates, self.register, self.customgates, self.measurements).simulate(return_full = True)
            return self.register, operations, self.final_measurements
        else: self.register = Simulator.Simulator(self.gates, self.register, self.customgates, self.measurements).simulate()

    def simulate2(self):
        """
        Applies the circuit to the initialized state vector using less memory than simulate()

        :return: The final state of the state vector
        
        """
        self.register, self.final_measurements = Simulator.Simulator(self.gates, self.register, self.customgates, self.measurements).simulate2()
        return self.register, self.final_measurements

    def addmeasure(self):
        """
        Adds a space where a measurement should be made. Mesurements are only made when simulating the circuit.

        """
        self.measurements.append(self.gateindex)
        for i in range(len(self.gates)):
            self.gates[i].append('i')
        self.gateindex += 1

    def show_results(self):
        """
        Prints out the initial definition of the statevector, along with the gates of the circuit.
        It then simulates the circuit and prints out the new statevector.

        """
        print('Register defined as:')
        print(self.register)
        #self.register.measure()
        print('Gates are:')
        print(np.array(self.gates, dtype = object), '\n')
        
        self.simulate2()
        print('Final state of the register is:')
        print(self.register)
        print('With statevector')
        print(self.register.Statevec)
        self.register.measure()
        
    def return_measurements(self):
        """
        Returns final measurements after simulation.
        """
        self.simulate2()
        return self.final_measurements
    
if __name__ == '__main__':
    pass