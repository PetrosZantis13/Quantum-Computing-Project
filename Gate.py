'''
Quantum Computing Project 
Author: Petros Zantis

The following class, Gate, is used to describe 
'''
import numpy as np

class Gate(object):
    
    '''
    Below is the constructor of the class, 
    '''
    def __init__(self, name):
        
        self.name = name
        gate = np.identity(2)  #in case the input name is wrong, return identity
        self.qbitdim = 1
        
        if(self.name=='Hadamard'):
            gate = np.ones((2,2))
            gate[1,1] = -1
            gate *= 1/np.sqrt(2)
            
        elif(self.name=='X'):
            gate = np.zeros((2,2))
            gate[0,1] = 1
            gate[1,0] = 1
            
        elif(self.name=='Y'):
            gate = np.zeros((2,2), dtype=complex)
            gate[0,1] = -1j
            gate[1,0] = 1j
            
        elif(self.name=='Z'):
            gate = np.identity(2)
            gate[1,1] = -1
        
        elif(self.name=='CNOT'):
            gate = np.zeros((4,4))
            gate[0,0] = 1
            gate[1,1] = 1
            gate[2,3] = 1
            gate[3,2] = 1
            self.qbitdim = 2
            
        elif(self.name=='CZ'):
            gate = np.identity(4)
            gate[3,3] = -1
            self.qbitdim = 2
        
        elif(self.name=='SWAP'):
            gate = np.zeros((4,4))
            gate[0,0] = 1
            gate[1,2] = 1
            gate[2,1] = 1
            gate[3,3] = 1
            self.qbitdim = 2
         
#         elif(self.name=='Phase Kickback'):
            
                
        self.operator = gate
    
    '''
    Below is a method called apply, 
    '''
    def build_gate(self, matrix):   # for building other gates on the go
      
        self.operator = matrix
        self.qbitdim = int( np.log(len(matrix)) / np.log(2))
      
#     def apply(self, qubit):
#         
#         print(f"\nApplying the {self.name} gate to qubit\n{qubit.vector}:\n")
#         new = self.operator.dot(qubit.vector)
#         qubit.update_qubit(new)
