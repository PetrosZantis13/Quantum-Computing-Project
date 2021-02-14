'''
Quantum Computing Project 
Author: Petros Zantis

The following class, Gate, is used to describe 
'''
import numpy as np
from Qubit import Qubit
from TensorProduct import TensorProduct

class Gate(object):
    
    '''
    Below is the constructor of the class, 
    '''
    def __init__(self, name):
        
        self.name = name
        gate = np.identity(2)  #in case the input name is wrong, return identity
        
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
            
        elif(self.name=='CZ'):
            gate = np.identity(4)
            gate[3,3] = -1
        
        elif(self.name=='SWAP'):
            gate = np.zeros((4,4))
            gate[0,0] = 1
            gate[1,2] = 1
            gate[2,1] = 1
            gate[3,3] = 1
            
        self.operator = gate
    
    '''
    Below is a method called apply, 
    '''
      
#     def apply(self, qubit):
#         
#         print(f"\nApplying the {self.name} gate to qubit\n{qubit.vector}:\n")
#         new = self.operator.dot(qubit.vector)
#         qubit.update_qubit(new)
    

gate = Gate("X")
print(gate.operator)

qubit = Qubit(0,1)
qubit.apply_gate(gate)
print(qubit.vector) 

print("\nFrom page 25 of the slides (testing the tensor product):")
Hgate =  Gate("Hadamard").operator
print( TensorProduct([Hgate, np.identity(2), Hgate]).product )

zerozero = TensorProduct([Qubit(1,0).vector, Qubit(1,0).vector]).product
oneone = TensorProduct([Qubit(0,1).vector, Qubit(0,1).vector]).product

phi_plus = (zerozero + oneone)/(np.sqrt(2))
print(f"\nPhi+ Bell state (Theoretical): \n{phi_plus}")

qubit.apply_gate(Gate("Hadamard"))
control = TensorProduct([qubit.vector, Qubit(1,0).vector]).product
print(control)
# en dulefki epidi to tensor product eshi array gia output,
# prepi na kamo register class je na ta kamni jina manipulate
control.apply(Gate("CNOT"))
