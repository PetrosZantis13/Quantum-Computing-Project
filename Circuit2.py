'''
Quantum Computing Project 
Author: Petros Zantis
'''
import matplotlib.pyplot as plt
from Gate import Gate
from State import *
from Tensor import *

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 13

class Circuit(object):
    
    def __init__(self, name):
        '''
        The constructor of the Circuit class takes as argument the name
        of the desired circuit.
        ''' 
        self.name = name
        
    def run_circuit(self):
        '''
        A function to run the circuit according to the specified name.
        ''' 
        if(self.name=='Bell'):
            
            qbit_zero = Qubit(1,0)
            qbit_one = Qubit(0,1)
            zerozero = Tensor([qbit_zero.vector, qbit_zero.vector]).product
            oneone = Tensor([qbit_one.vector, qbit_one.vector]).product
            
            phi_plus = (zerozero + oneone)/(np.sqrt(2))
            print(f"\nPhi+ Bell state (Theoretical): \n{phi_plus}")
            
            qbit_zero.apply_gate(Gate("Hadamard"))
            control = Tensor([qbit_zero.vector, Qubit(1,0).vector]).product
            state = State(control)
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
            state = State(Tensor([qbit_one.vector, qbit_one.vector]).product)
            state.apply_gate(Gate("CZ"))
            print(state.vector)
            print("\nFrom page 25 of the slides (testing the tensor product):")
            Hgate =  Gate("Hadamard")
            H = Hgate.operator
            print( Tensor([H, np.identity(2), H]).product )
            
        elif(self.name=='Grover'):

            qbits = 6      # number of qubits, change to prompt later
            N = 2**qbits
            desired = State(BasisStates(N).states[13])   # which state to search for
            print(desired)
            qbit_zero = Qubit(1,0)
            qbit_zero.apply_gate(Gate("Hadamard"))
            input = []
            for i in range(qbits):
                input.append(qbit_zero.vector)
            state = State(Tensor(input).product)
            print(state.vector)
            
            R_matrix = 2*(Tensor([state.vector.T,state.vector]).product) - np.identity(N)
            R_gate = Gate("R")
            R_gate.build_gate(R_matrix)
            print(R_gate.operator) 
            print(R_gate.qbitdim)
            
            Uf_matrix = np.identity(N) - 2*(Tensor([desired.vector.T,desired.vector]).product)
            Uf_gate = Gate("Uf")
            Uf_gate.build_gate(Uf_matrix)
            print(Uf_gate.operator) 
            print(Uf_gate.qbitdim)  
            
            fig, ax = plt.subplots()
            self.plot_probs(state, ax)
            iter = 0
            while(np.max(state.probabilities()[1]) < 0.95 ):
                state.apply_gate(Uf_gate)
                state.apply_gate(R_gate)
                self.plot_probs(state, ax)
                iter += 1
                
            print(f"Grover's Algorithm with {qbits} qubits ({N} possible states)"+
                  f"\nterminated at {iter} iterations. (Sqrt({N}) = {np.sqrt(N)})")
        
    # maybe add a draw_circuit function?
        
    def plot_probs(self, state, ax):
        '''
        A function to plot the probability of each state as a bar chart. 
        ''' 
        plt.cla() 
        states, amps = state.probabilities()           
        plt.bar(states, amps)
        ax.set_xlabel("State | i >")
        ax.set_xticks(states)
        ax.set_ylabel("Probability")
        ax.set_yticks(np.arange(0,1.1,0.1))
        ax.set_ylim(0,1.0)
        ax.set_title("Grover's algorithm picking out desired state")
        plt.pause(0.5)
        
c = Circuit("Gates Test")
c.run_circuit()
c = Circuit("Bell")
c.run_circuit()
c = Circuit("Grover")
c.run_circuit()

# for Grovers maybe do a while loop, when prob is >95%, output n, show rootN relationship
# also abstract this to return a string from a random list

# ALSO, try quantum teleportation and error correction?
