'''
Quantum Computing Project 
Author: Petros Zantis
'''
import numpy as np

class Gate(object):
    
    def __init__(self, name):
        '''
        The constructor of the Gate class, taking as argument the name
        of the desired gate and building it accordingly.
        '''
        self.name = name
        gate = np.identity(2)  # defaults to the 2x2 identity
        self.qbitdim = 1    # defaults to a single-qubit gate
        
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
            self.qbitdim = 2    # double-qubit gate
            
        elif(self.name=='CZ'):
            gate = np.identity(4)
            gate[3,3] = -1
            self.qbitdim = 2    # double-qubit gate
        
        elif(self.name=='SWAP'):
            gate = np.zeros((4,4))
            gate[0,0] = gate[1,2] = 1            
            gate[2,1] = gate[3,3] = 1            
            self.qbitdim = 2   # double-qubit gate
         
#         elif(self.name=='Phase Shift' or Rphi):   
                
        self.operator = gate
    
    def build_gate(self, matrix):
        '''
        A function for building other custom gates on the go
        '''
        self.operator = matrix
        self.qbitdim = int( np.log(len(matrix)) / np.log(2))
