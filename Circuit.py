'''
Quantum Computing Project 
Author: Petros Zantis

The following class, Gate, is used to describe 
'''
import numpy as np
import matplotlib.pyplot as plt
from Qubit import Qubit
from TensorProduct import TensorProduct
from Entangled import Entangled
from Gate import Gate
from BasisStates import BasisStates
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 13

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
            #state.probabilities()
            state.apply_gate(Gate("CNOT"))
            print(state.vector)
            
        elif(self.name=='Gates Test'):
            
            X = Gate("X")
            print("X single qubit gate:")
            print(X.operator)
            qbit_zero = Qubit(1,0)
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
            
        elif(self.name=='Grover'):

            N = 5       # number of qubits, change to prompt later
            desired = Entangled(BasisStates(2**N).states[5])   # which state to search for
            print(desired)
            qbit_zero = Qubit(1,0)
            qbit_zero.apply_gate(Gate("Hadamard"))
            input = []
            for i in range(N):
                input.append(qbit_zero.vector)
            state = Entangled(TensorProduct(input).product)
            print(state.vector)
            
            R_matrix = 2*(TensorProduct([state.vector.T,state.vector]).product) - np.identity(2**N)
            R_gate = Gate("R")
            R_gate.build_gate(R_matrix)
            print(R_gate.operator) 
            print(R_gate.qbitdim)
            
            Uf_matrix = np.identity(2**N) - 2*(TensorProduct([desired.vector.T,desired.vector]).product)
            Uf_gate = Gate("Uf")
            Uf_gate.build_gate(Uf_matrix)
            print(Uf_gate.operator) 
            print(Uf_gate.qbitdim)  
            
            fig, ax = plt.subplots()
            self.animate(state, ax)
            while(True):
                state.apply_gate(Uf_gate)
                state.apply_gate(R_gate)
                self.animate(state, ax)
                
# maybe add a run_circuit function? 
# maybe add a draw function?
    
    def animate(self, state, ax):  # animate_plot
        
        plt.cla() 
        x, amps = state.probabilities()           
        plt.bar(x, amps)
        ax.set_xlabel("State | i >")
        ax.set_xticks(x)
        ax.set_ylabel("Probability")
        ax.set_yticks(np.arange(0,1.1,0.1))
        ax.set_ylim(0,1.0)
        ax.set_title("Grover's algorithm picking out desired state")
        plt.pause(0.5)
        
Circuit("Gates Test")
Circuit("Bell")
Circuit("Grover")

# for Grovers maybe do a while loop, when prob is >95%, output n, show rootN relationship
# also abstract this to return a string from a random list

# ALSO, try quantum teleportation and error correction?
