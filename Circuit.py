'''
Quantum Computing Project 
Author: Petros Zantis

The following class, Gate, is used to describe 
'''
import numpy as np
from Qubit import Qubit
from TensorProduct import TensorProduct
from Entangled import Entangled
from Gate import Gate

class Circuit(object):
    
    '''
    Below is the constructor of the class, 
    '''
    def __init__(self, name):
        
        self.name = name
        
        if(self.name=='Bell'):
            
            qbit_zero = Qubit(1,0)
            qbit_one = Qubit(0,1)
            zerozero = TensorProduct([qbit_zero.vector, qbit_zero.vector]).product
            oneone = TensorProduct([qbit_one.vector, qbit_one.vector]).product
            
            phi_plus = (zerozero + oneone)/(np.sqrt(2))
            print(f"\nPhi+ Bell state (Theoretical): \n{phi_plus}")
            
            qbit_zero.apply_gate(Gate("Hadamard"))
            control = TensorProduct([qbit_zero.vector, Qubit(1,0).vector]).product
            state = Entangled(control)
            print(state.vector)
            state.apply_gate(Gate("CNOT"))
            print(state.vector)
            

# maybe add a run_circuit function? 
# maybe add a draw function?

X = Gate("X")
print("X single qubit gate:")
print(X.operator)
qbit_zero = Qubit(0,1)
qbit_zero.apply_gate(X)
print(qbit_zero.vector) 
print()
cz = Gate("CZ")
print("CZ double qubit gate:")
print(cz.operator)
qbit_zero = Qubit(1,0)
qbit_one = Qubit(0,1)
state = Entangled(TensorProduct([qbit_one.vector, qbit_one.vector]).product)
state.apply_gate(Gate("CZ"))
print(state.vector)

print("\nFrom page 25 of the slides (testing the tensor product):")
Hgate =  Gate("Hadamard")
H = Hgate.operator
print( TensorProduct([H, np.identity(2), H]).product )

#Circuit("Bell")


