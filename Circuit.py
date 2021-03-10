"""
The Circuit Module calls the Circuit class to build any pre-defined circuit available by providing a name
(e.g. “Grover”, “Teleportation”), and then calls the run_circuit() function on the created Circuit objects to run them.
"""
import matplotlib.pyplot as plt
from Interface import Interface
from Tensor import *
from Gate import *
from State import *
import copy

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 13

class Circuit(Interface):
    """
    Defines the circuit of the algorithm. Checks that the  prompts are of the correct formats.

    """ 
    
    def __init__(self, name): 
        super().__init__(name)     
    
    def run_circuit(self):        
        """
        A function to run the circuit according to the specified name.
        """
        print(f"\nRunning {self.name} Circuit") 
        
    def show_results(self):        
        """
        A function to show the results obtained according to the circuit
        being run/tested.
        """
        print(f"\nShowing {self.name} Circuit Results")
    
    def size_prompt(self):        
        """
        A function to prompt for the system size, catching any possible errors on the way.     
        """    
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
        """
        A function to prompt for a qubit. Only accepts 0 or 1.
        """     
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
    
    def AorM_prompt(self):
        """
        A function to prompt for an animation/measurement.
        """  
        AorM = input("\nPlease type 'a' for Animation or 'm' for Measurements: ")
    
        if(AorM=='a'):            
            print("Animation")
            
        elif(AorM=='m'):            
            print("Measurements")
            
        else:
            print("Invalid entry. Please try again.")
            AorM = self.AorM_prompt()
        
        return AorM 

class Bell(Circuit):
    """
    Creates Bell States by applying the necessary Gates.
    """ 
    
    def __init__(self): 

        super().__init__("Bell States")
    
    def run_circuit(self):
        """
        Runs the circuit with the given Bell States

        :return: Bell States
        """
        
        super().run_circuit()
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
            state = control.to_state()
            state.apply_gate(Gate("CNOT"))
            print(state.vector)
            Bell_states.append(state)
            
        return Bell_states  
     
class Grover(Circuit):
    """
    Implementation of Grover's algorithm. Runs the circuit with the specified gates and visualizes the result of the algorithm.
    """ 
    
    def __init__(self): 
        super().__init__("Grover") 
        
    def prep_circuit(self):
        """
        Preparation of circuit

        :return: qbits of the circuit, desired state to look for and the prompt for animation/measurements
        """
        
        AorM = self.AorM_prompt()
            
        if(AorM=='a'):        
            qbits = super().size_prompt()     # number of qubits 
            reps = 1 
            d = input("Choose the desired state to search for: ")
            wrong = True
            while(wrong):
                try:                         
                    d = int(d)
                    if( (d<(2**qbits)) and d>=0 ):      # ensure N is an integer larger than 0
                        wrong = False
                    else:
                        d = int("zero")  # ValueError
                except ValueError:
                    print(f"Please enter a valid integer smaller than {2**qbits}.")
                    d = input("Choose the desired state to search for: ")   
        
            return qbits, d, AorM
        
        elif(AorM=='m'):
            qbits = np.arange(2,13,1)
            d = 1
            
            iters=[]
            for qs in qbits:
                iter, success = self.run_circuit(qs, d, AorM)
                iters.append(iter)
             
            self.show_results(qbits, iters)    
            
            qbits = np.arange(2,11,1)
            reps = 500    
            successes = []
            for qs in qbits:
                count = 0
                for rep in range(reps):                        
                    iter, success = self.run_circuit(qs, d, AorM)
                    count += success
                successes.append( (count/reps)*100)
                    #self.show_results(qbits, successes)
            plt.title("Percentage accuracy of Grover search\nover number of qubits in the system")
            plt.plot(qbits, successes)
            plt.xlabel("Number of qubits")
            plt.ylabel("Percentage accuracy")
            plt.ylim(50,100)
            plt.show()            
        
    def run_circuit(self, *args):
        """
        Run of the circuit with the Grover's algorithm

        :return: number of iterations needed to terminate and the success of finding the desired state in Grover's algorithm (1 for success, 0 for failure)
        """
        
        super().run_circuit()
        
        if(not args):
            unpacked = self.prep_circuit()
            if(unpacked!= None):
                qs, d, AorM = unpacked
            else:
                return
        else:
            qs, d, AorM = args
        
        print(f"Now running with {qs} qubits")
        N = 2**qs
        desired = State(BasisStates(N).states[d])   # which state to search for
        qbit_zero = Qubit(1,0)
        qbit_zero.apply_gate(Gate("Hadamard"))
        reg = []
        for i in range(qs):
            reg.append(qbit_zero)
        
        register = Tensor(reg)
        state = register.to_state()
        print(f"\nThe initial state vector (register) is:\n{state.vector}")
        
        oracle = Tensor([desired,desired])
        oracle.calculate()
        Uf_matrix = np.identity(N) - 2*(oracle.product.reshape(N,N))
        Uf_gate = Gate("Uf")
        Uf_gate.build_gate(Uf_matrix)
        print(f"\nThe Oracle operator is:\n{Uf_gate.operator}")
        #print(Uf_gate.qbitdim)  
        
        diffusion = Tensor([state,state])
        diffusion.calculate()
        R_matrix = 2*(diffusion.product.reshape(N,N)) - np.identity(N)
        R_gate = Gate("R")
        R_gate.build_gate(R_matrix)
        print(f"\nThe Diffusion operator is:\n{R_gate.operator}")
        #print(R_gate.qbitdim)
        
        if(AorM=='a'): 
            fig, ax = plt.subplots()
            self.plot_probs(state, ax)
        #iter = 0
        #while(np.max(state.probabilities()[1]) < 0.9 ):
        iter = int( (np.pi/4) * np.sqrt(N) )
        for i in range(iter):
            state.apply_gate(Uf_gate)
            state.apply_gate(R_gate)
            if(AorM=='a'): 
                self.plot_probs(state, ax)
            #iter += 1
        
        collapsed = state.measure()
        print(f"The desired state was {d}, and the quantum state collapsed to {collapsed}.")
        if (d == collapsed):
            print("Succesful search!")
            success =1 
            print(f"\nGrover's Algorithm with {qs} qubits ({N} possible states)"+
                  f"\nterminated at {iter} iterations. (Sqrt({N}) = {np.sqrt(N)})\n")
        else:
            print("Unsuccesful search.") 
            success =0
        
        if(AorM=='a'): 
            plt.close(fig)
            
        return iter, success
           
    def plot_probs(self, state, ax):
        """
        A function to plot the probability of each state as a bar chart. 

        """ 

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
        
    def show_results(self, qubits, iters):
        """
        A function to run Grover's algorithm with various numbers of qubits
        and plot the resulting iterations, comparing it to the predicted 
        O(sqrtN) and the classical O(N)
        """ 
        super().show_results()           
        print(iters)        
        plt.plot(qubits, 2**qubits, label = "O(N)")
        plt.plot(qubits, 2**(qubits/2), label = r'O($\sqrt{N}$)')
        plt.plot(qubits, iters, label = "Grover's trials")
        plt.xticks(qubits)
        plt.xlabel("Number of qubits in the system")
        plt.ylabel("Total number of states N")
        plt.yscale("log")
        plt.legend()
        #plt.title("Time complexity over number of qubits in the system")
        plt.show()
        
class Teleportation(Circuit):
    """
    Begins by initializing Alice’s and Bob’s qubits to the user’s selection. The program then stores the state of the quantum channel, and proceeds to entangle Alice’s 
    qubit with the unknown one. Next, a Bell measurement takes place which collapses this entangled state to one of four possible Bell states. 
    According to the result, a correction gate is applied to Bob’s qubit, which is then measured on the computational basis to give either 0 or 1. 
    """
    
    def __init__(self): 
        """
        The constructor of the Circuit class takes as argument the name
        of the desired circuit.
        """ 
        super().__init__("Teleportation")    
        
    def prep_circuit(self):
        """
        Preparation of circuit

        :return: Alice's qubit and Bob's qubit
        """
        
        AorM = self.AorM_prompt()
            
        if(AorM=='a'):
        
            print("Alice's qubit:")
            a = self.qubit_prompt()
            print("Bob's qubit:")
            b = self.qubit_prompt()
            runs = 1
            return a, b, 0.8, 0.6
        
        elif(AorM=='m'):
            a=b=zeros=ones=0  # test other scenarios
            alpha = 0.8
            beta = 0.6
            runs = 500
            errors_a =[] 
            errors_b =[] 
        
            for run in range(1,runs+1):
                Bob = self.run_circuit(a, b, alpha, beta)              
            
                if(Bob==0):
                    zeros+=1
                elif(Bob==1):
                    ones+=1
            
                a_temp = np.sqrt(zeros/runs)
                b_temp = np.sqrt(ones/runs)
                print(f"\nBob's teleported state (at {run} runs):")
                print(f"{a_temp:.4f} |0> + {b_temp:.4f} |1>")
                error_a = np.abs( (alpha - a_temp) /alpha)
                error_b = np.abs( (beta - b_temp) /beta)
                errors_a.append(error_a)
                errors_b.append(error_b)  
            
            self.show_results(errors_a, errors_b)                      
    
    def run_circuit(self, *args):
        """
        Run of the circuit for Teleportation.

        :return: collapsed state as measured by Bob.

        """
        super().run_circuit()
        
        if(not args):
            unpacked = self.prep_circuit()
            if(unpacked!= None):
                a, b, alpha, beta = unpacked
            else:
                return
        else:
            a, b, alpha, beta = args  #CONTINUE FIXING THIS TOMORROW
        
        Bell_circuit = Bell()
        Bell_states = Bell_circuit.run_circuit()
        
        qbit_alice = Qubit(1-a,a)     
        qbit_bob = Qubit(1-b,b)
                    

        #Entangle the 2 qubits in one of the 4 Bell states (Quantum Channel)
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
                
        #Alice's entangles her two qubits and performs a Bell measurement
        qbit_unknown = Qubit(alpha, beta)  #Qubit(0.28,0.96)   
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
        collapsed_Bob = qbit_bob.measure()
        print(f"\nFinally, Bob measures his qubit in state |{collapsed_Bob}>.")
        return collapsed_Bob
        
    def show_results(self, errors_a, errors_b):
        """
        A function to show results of teleportation
        """ 
        super().show_results()                   
        plt.plot(errors_a, label = r'$\alpha$')
        plt.plot(errors_b, label = r'$\beta$')
        plt.xticks()  # runs
        plt.xlabel("Number of runs")
        plt.ylabel("Relative error")
        plt.title("Teleportation")
        plt.legend()
        plt.show()
  
def main():
    """
    Runs both Grover and Teleportation Implementations
    """
    
    b = Bell()
    b.run_circuit() 
    g = Grover()
    g.run_circuit()
    t = Teleportation()
    t.run_circuit()

if __name__ == "__main__":
    main()
        