'''
Quantum Computing Project 
Author: Petros Zantis
'''
import matplotlib.pyplot as plt
from Tensor import *
from Gate import *
from State import *
import copy

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 13

class Circuit(object):
    
    def __init__(self, name):
        '''
        The constructor of the Circuit class takes as argument the name
        of the desired circuit.
        ''' 
        self.name = name        
    
    def size_prompt(self):        
        '''
        A function to prompt for the system size, catching any possible errors on the way.     
        '''     
        qbits = input("Type in the system size in qubits: ")
        wrong = True
        while(wrong):
            try:                         
                qbits = int(qbits)
                if(qbits>0):      # ensure N is an integer larger than 0
                    wrong = False
                else:
                    qbits = int("zero")  # ValueError
            except ValueError:
                print("Please enter a valid integer larger than 0.")
                qbits = input("Type in the system size N: ")
        
        return qbits 

    def qubit_prompt(self):        
        '''
        A function to prompt for a qubit. Only accepts 0 or 1.
        '''     
        qbit = input("Choose 0 or 1: ")
        wrong = True
        while(wrong):
            try:                         
                qbit = int(qbit)
                if(qbit == 0 or qbit == 1): # ensure qubit is either zero or one
                    wrong = False
                else:
                    qbit = int("zero")  # ValueError
            except ValueError:
                print("Invalid entry. Please select between 0 or 1.")
                qbit = input("Choose 0 or 1: ")
        
        return qbit  
    
    def run_circuit(self):
        '''
        A function to run the circuit according to the specified name.
        ''' 
        if(self.name=='Bell States'):
            
            qbit_zero = Qubit(1,0)
            qbit_one = Qubit(0,1)
            inputs = [qbit_zero, qbit_one]
            Bell_states = []
            
            for i in range(4):
                print(f"\nPreparing Bell State with qubits |{int(i/2)}> and |{i%2}> :")
                qbit_a = copy.copy(inputs[i%2])
                qbit_b = copy.copy(inputs[int(i/2)])                                                          
                qbit_a.apply_gate(Gate("Hadamard"))
                control = Tensor([qbit_a, qbit_b])
                control.calculate()
                state = State(control.product)
                state.apply_gate(Gate("CNOT"))
                print(state.vector)
                Bell_states.append(state)
                
            return Bell_states        
        
        elif(self.name=='Grover'):

            qbits = self.size_prompt()     # number of qubits
            N = 2**qbits
            desired = State(BasisStates(N).states[1])   # which state to search for
            qbit_zero = Qubit(1,0)
            qbit_zero.apply_gate(Gate("Hadamard"))
            input = []
            for i in range(qbits):
                input.append(qbit_zero)
            
            register = Tensor(input)
            register.calculate()
            state = State(register.product)
            print(state.vector)
            
            oracle = Tensor([desired,desired])
            oracle.calculate()
            Uf_matrix = np.identity(N) - 2*(oracle.product.reshape(N,N))
            Uf_gate = Gate("Uf")
            Uf_gate.build_gate(Uf_matrix)
            print(Uf_gate.operator) 
            print(Uf_gate.qbitdim)  
            
            diffusion = Tensor([state,state])
            diffusion.calculate()
            R_matrix = 2*(diffusion.product.reshape(N,N)) - np.identity(N)
            R_gate = Gate("R")
            R_gate.build_gate(R_matrix)
            print(R_gate.operator) 
            print(R_gate.qbitdim)
            
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
            
            plt.close(fig)
            return iter
        
        elif(self.name=='Teleportation'):
            
            AorM = self.prompt()
            
            if(AorM=='a'):
            
                print("Alice's qubit:")
                a = self.qubit_prompt()
                print("Bob's qubit:")
                b = self.qubit_prompt()
                runs = 1
            
            else:
                a=b=zeros=ones=0  # test other scenarios
                runs = 1000
            
            for i in range(runs):  
                 
                qbit_alice = Qubit(1-a,a)     
                qbit_bob = Qubit(1-b,b)    
                
                Bell_circuit = Circuit("Bell States")
                Bell_states = Bell_circuit.run_circuit()            
                '''
                Entangle the 2 qubits in one of the 4 Bell states (Quantum Channel)
                '''
                qbit_alice.apply_gate(Gate("Hadamard"))            
                control = Tensor([qbit_alice, qbit_bob])
                control.calculate()
                entangled_AB = State(control.product)
                entangled_AB.apply_gate(Gate("CNOT"))
                
                for idx, Bell_state in enumerate(Bell_states):
                    if(entangled_AB.vector.T.dot(Bell_state.vector) > 0 ):                        
                        AB_index = idx   
                        print(f"\nQuantum Channel is in Bell State {AB_index}:")
                        print(entangled_AB.vector)
                        
                '''
                Alice's entangles her two qubits and performs a Bell measurement
                '''    
                qbit_unknown = Qubit(0.8,0.6)  #Qubit(0.28,0.96)   
                #print(qbit_unknown.probabilities())
                #qbit_unknown.apply_gate(Gate("Hadamard"))            
                control = Tensor([qbit_unknown, qbit_alice])
                control.calculate()
                entangled_AC = State(control.product)
                entangled_AC.apply_gate(Gate("CNOT"))
                print(f"\nAlice entangles the unknown state with her qubit to:")
                print(entangled_AC.vector)
                #print(entangled_AC.probabilities())
                print(f"\nTransformed to Bell Bases:")
                #entangled_AC.apply_gate(Gate("CNOT"))
                reverse = Tensor([Gate('I'), Gate('H')])
                reverse.calculate()
                tr_gate = Gate("Transform")
                tr_gate.build_gate(reverse.product)
                entangled_AC.apply_gate(tr_gate)
                
                print(entangled_AC.vector)
                #PETRO HERE TRANSFORM THIS TO BELL BASIS BEFORE MEASUREMENT
                print(f"\nAlice measures her entangled state:")
                AC_index = entangled_AC.measure()            
                print(f"\nAlice's measurement gave out Bell State {AC_index}:")
                print(Bell_states[AC_index].vector)
                
                diff = AC_index - AB_index
                
                if( diff == 0):
                    print("\nBob's qubit is already in desired state")
                    corr_gate = Gate("I")
                    
                elif( diff == 1 or diff == -3):
                    corr_gate = Gate("Z")
                elif( np.abs(diff) == 2):
                    corr_gate = Gate("X")
                elif( diff == 3 or diff == -1):
                    correction = (Gate("Z").operator).dot(Gate("X").operator)
                    corr_gate = Gate("ZX")
                    corr_gate.build_gate(correction)
                
                print(f"\nThe appropriate correction is:\n{corr_gate.operator}")
                qbit_bob.apply_gate(corr_gate)
                print("\nBob's qubit after applying correction:")
                print(qbit_bob.vector)
                
                if(AorM=='m'):
                    if(np.all(qbit_bob.vector == Qubit(1,0).vector)):
                        zeros+=1
                    elif(np.all(qbit_bob.vector == Qubit(0,1).vector)):
                        ones+=1
                    
                    print(f"\nBob's teleported state ({runs} runs):")
                    print(f"{np.sqrt(zeros/runs):.4f} |0> + {np.sqrt(ones/runs):.4f} |1>")
            
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
        
    def grover_data(self):
        '''
        A function to run Grover's algorithm with various numbers of qubits
        and plot the resulting iterations, comparing it to the predicted 
        O(sqrtN) and the classical O(N)
        ''' 
        qs = np.arange(2,8,1)
        iters = []
        for q in qs:
            print(q)
            c = Circuit("Grover")
            iter = c.run_circuit()
            iters.append(iter)
            
        plt.plot(qs, 2**qs, label = "O(N)")
        plt.plot(qs, 2**(qs/2), label = r'O($\sqrt{N}$)')
        plt.plot(qs, iters, label = "Grover's trials")
        plt.xticks(qs)
        plt.xlabel("Number of qubits in the system")
        plt.ylabel("Total number of states N")
        plt.legend()
        plt.show()
        
    def prompt(self):
        
        AorM = input("Please type 'a' for Animation or 'm' for Measurements: ")
    
        if(AorM=='a'):
            
            print("Animation:")
            
        elif(AorM=='m'):
            
            print("Measurements:")
            
        else:
            print("Invalid entry. Please try again.")
            self.prompt()
        
        return AorM
    
#c = Circuit("Grover")
#c.run_circuit()
t = Circuit("Teleportation")
t.run_circuit()

# ALSO, try quantum teleportation and error correction?

'''
THESE BELOW ARE ALL RUNTIME TESTS SO IGNORE THEM
'''
# print("An example of Basis States:")
# print(BasisStates(4).vector)      

# zeros = 0
# ones = 0
# runs = 10000
# for i in range(runs):
#     test = Qubit(0.8,0.6)
#     #print(test.probabilities())
#     test.measure()
#     if(np.all(test.vector == Qubit(1,0).vector)):
#         zeros+=1
#     elif(np.all(test.vector == Qubit(0,1).vector)):
#         ones+=1
#     #print(test.probabilities())
#      
# print(f"{zeros/runs} |0> + {ones/runs} |1>")
# 
# qbit_zero = Qubit(1,0)
# qbit_zero.apply_gate(Gate("Hadamard"))
# input = []
# for i in range(2):
#     input.append(qbit_zero.vector)
# state = State(Tensor(input).product)
# print(state.probabilities()[1])
# runs = 5
# finals = np.zeros(len(state.vector))
# 
# for i in range(runs):
#     state = State(Tensor(input).product)
#     collapsed = state.measure()
#     finals[collapsed] += 1
# 
# print(finals/runs)    

# qbit_zero = Qubit(1,0)
# qbit_zero.apply_gate(Gate("Hadamard")) 
# qbit_h = Qubit(1,0)
# qbit_h.apply_gate(Gate("Hadamard"))
# register = Tensor([qbit_zero, qbit_h])
# register.calculate()
# print(register.product)
# 
# qbit_h.measure()
# print(qbit_h.vector)
# register.calculate()
# print(register.product)
# print()
# gate = Gate('X')
# register = Tensor([Gate('Hadamard'), Gate('I'), Gate('Hadamard')])
# register.calculate()
# print(register.product)

# qbit_zero = Qubit(1,0)
# qbit_one = Qubit(0,1)
# register = Tensor([qbit_one, qbit_zero])
# register.calculate()
# state = State(register.product)
# print(state.vector)
# cnot = Gate("CNOT")
# print(cnot.operator)
# state.apply_gate(cnot)
# print(state.vector)

# ans = c.qubit_prompt()
# print(f"{1-ans},{ans}")
