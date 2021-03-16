"""
The Gate module is used to create objects representing quantum gates. 
It then builds the matrix representation of the operator accordingly and 
saves this as an attribute, along with a value representing the qubit-dimension 
of the gate, for example 1 for single-qubit or 2 for double-qubit gates. 
"""
import numpy as np

class Gate(object):
    
    def __init__(self, name):
        """ The constructor of the Gate class.

        :param name:  name of the desired gate
        """
        self.name = name
        # defaults to the 2x2 identity
        gate = np.identity(2)
        # defaults to a single-qubit gate
        self.qbitdim = 1 
        
        if(self.name=='Hadamard' or self.name=='H'):
            gate = np.ones((2,2))
            gate[1,1] = -1
            gate *= 1/np.sqrt(2)
            
        elif(self.name=='X'):
            gate = np.zeros((2,2))
            gate[0,1] = gate[1,0] = 1            
            
        elif(self.name=='Y'):
            gate = np.zeros((2,2), dtype=complex)
            gate[0,1] = -1j
            gate[1,0] = 1j
            
        elif(self.name=='Z'):
            gate = np.identity(2)
            gate[1,1] = -1
        
        elif(self.name=='CNOT' or self.name=='CX'):
            gate = np.zeros((4,4))
            gate[0,0] = gate[1,1] = 1            
            gate[2,3] = gate[3,2] = 1  
            # double-qubit gate         
            self.qbitdim = 2    
            
        elif(self.name=='CZ'):
            gate = np.identity(4)
            gate[3,3] = -1
            # double-qubit gate
            self.qbitdim = 2   
        
        elif(self.name=='SWAP'):
            gate = np.zeros((4,4))
            gate[0,0] = gate[1,2] = 1            
            gate[2,1] = gate[3,3] = 1  
            # double-qubit gate          
            self.qbitdim = 2   
                         
        self.operator = gate
    
    def build_gate(self, matrix):
        """Builds other custom gates on the go

        :param matrix: Matrix that defines the gate 
        """
        self.operator = matrix
        self.qbitdim = int( np.log(len(matrix)) / np.log(2))
