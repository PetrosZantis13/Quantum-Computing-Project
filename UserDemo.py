# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:30:35 2021

@author: mikva
"""
from QuantumCircuit import *
import Presentation
from Circuit import *
import numpy as np
import matplotlib.pyplot as plt
import time
import Sparse

def timeBenchmarks():
    
    qbits = np.arange(2,9,1)   # mihaly's limit is 8 qubits, mine is 12
    times = np.zeros((3,len(qbits)))
    
    for q in qbits:
        
        t1 = time.time()           
        Presentation.Grover_Circuit(q, [3], plot_results=False)
        t2 = time.time()
        times[0,q-2] = t2-t1
          
        t1 = time.time()
        Presentation.LazyGroverDemo(q, [3], plot_results=False)
        t2 = time.time()
        times[1,q-2] = t2-t1
        
        t1 = time.time()
        g = Grover()
        g.run_circuit(q,1,'m')        
        t2 = time.time()
        times[2,q-2] = t2-t1
        
    plt.plot(qbits, times[0], label='sparse')
    plt.plot(qbits, times[1], label='lazy')
    plt.plot(qbits, times[2], label='numpy')
    plt.title("Runtime of Grover's Algorithm over Number of Qubits in the system")
    plt.xlabel("Number of Qubits")
    plt.ylabel("Runtime (s)")
    plt.yscale("log")
    plt.legend()
    plt.show()
    
def tensorTest():
    
    loops = 17
    print(f"\nChecking the time it takes for each of the two implementations\nto do a tensor product of {loops} items:")
    
    v1 = Sparse.Vector(np.array([1,0]))
    result = Sparse.Vector(np.array([1,0]))
    t1 = time.time()
    for i in range(loops):
        result = result.outer(v1)
    t2 = time.time()
    print(f"\nResult 1 :\n {result} ")
    print(f"Time taken : {t2-t1} ")
    
    t1 = time.time()
    qbit_zero = Qubit(1,0)
    reg = []
    for i in range(loops):
        reg.append(qbit_zero)
    
    register = Tensor(reg)
    state = register.to_state()
    t2 = time.time()
    print(f"\nResult 2 :\n {state.vector.T} ")
    print(f"Time taken : {t2-t1} ")

def compareProbabilities():
    
    lazy_max_measures = []
    numpy_max_measures = []
    # 2-9 qubits
    measured_bits = 1
    for n_qubits in range(2,8):
        lazy_max_measures.append([])
        grover_circuit = QuantumCircuit('Grover', n_qubits)
        repetitions = int(np.pi/4*np.sqrt(2**n_qubits)) - 1
        grover_circuit.addGate('h', [i for i in range(n_qubits)])
        grover_circuit.addmeasure()
        # calculate oracle
        oracle = Sparse.ColMatrix(2**n_qubits)
        for i in range(2**n_qubits):
            if i in [measured_bits]:
                oracle[i,i] = -1
            else: oracle[i,i] = 1

        #Add Oracle
        grover_circuit.addCustom(0, n_qubits-1, oracle, 'oracle')
        #Add diffuser
        Presentation.diffuser(grover_circuit)
    
        grover_circuit.addmeasure()
        # Repeat if necessary
        for i in range(repetitions):
            # Add Oracle
            grover_circuit.addCustom(0, n_qubits-1, oracle, 'oracle')
            #Add diffuser
            Presentation.diffuser(grover_circuit)
            grover_circuit.addmeasure()    
    
        #show results
        final_statevec, measurements = grover_circuit.lazysim()
        for m in measurements[1]:            
            lazy_max_measures[n_qubits-2].append(max(m*m.conj()))
        
        g = Grover()    
        iter, success, desired_amps = g.run_circuit(n_qubits, 1,'testing')
        numpy_max_measures.append(desired_amps)
        
    print("Checking if the two implementations produce the same results:")
    print(f"\nResult 1 :")
    print(np.array(lazy_max_measures, dtype=object))
    print(f"\nResult 2 :")
    print(np.array(numpy_max_measures, dtype=object))   
    
def BorD_prompt():
    """
    A function to prompt for benchmark or demonstration.
    """  
    BorD = input("\nPlease type 'd' for Demonstrations or 'b' for Benchmarks: ")

    if(BorD=='b'):
        BorD = "benchmarks"            
        print("Benchmarks")
        
    elif(BorD=='d'):
        BorD = "demo"             
        print("Demonstration")
        
    else:
        print("Invalid entry. Please try again.")
        BorD = BorD_prompt()
    
    return BorD 

def builder_prompt():
    """
    A function to prompt for circuit-builder or pre-built circuits.
    """  
    build = input("\nPlease type 'p' for pre-built circuits or 'b' for circuit-builder: ")

    if(build=='p'):           
        print("Pre-built circuits")
        build = circuit_prompt()
        
    elif(build=='b'):
        build = 'builder'            
        print("Circuit builder")
        
    else:
        print("Invalid entry. Please try again.")
        build = builder_prompt()
    
    return build 

def circuit_prompt():
    """
    A function to prompt for circuit-builder or pre-built circuits.
    """  
    circ = input("\nPlease type 'b' for Bell States circuit, 'g' for Grover circuit,\nor 't' for Teleportation circuit:")
    while(circ!='b' and circ!='g' and circ!='t'):           
        print("Invalid entry. Please try again.")
        circ = circuit_prompt()
        
    if circ=='b':
        circ = "Bell States"
    elif circ=='g':
        circ = "Grover"
    elif circ=='t':
        circ = "Teleportation"
        
    return circ 

def circuit_builder_prompt():
    """
    Function to determine which circuit to build for the user.
    """
    circ = input("\nWhich circuit would you like to build?\nType 'grover' for Grover's circuit or 'BV' for a Bernstein-Vazirani circuit.\n")
    if circ=='grover':
        return circ
    if circ=='BV':
        return circ
    else:
        print('Invalid entry')
        return circuit_builder_prompt()

def actual_builder(algorithm):
    """
    Function which builds the circuit as prompted by the user.
    """
    if algorithm=='grover':
        size = int(input("\nPlease enter the size of the desired circuit\n"))
        state = int(input("\nPlease enter the desired state\n"))
        if state<2**size:
            Presentation.LazyGroverDemo(size, [state])
        else: 
            print("\nSomething went wrong. \nThe desired state might be out of bounds")
            actual_builder('grover')
    
    elif algorithm=='BV':
        mystery_string = str(input("\nPlease enter a mystery bitstring (i.e. a bunch of 1s and 0s)"))
        Presentation.Ber_Vaz(mystery_string)
        print("Your mystery string was:", mystery_string)
        print("Does it match the qubits in the register?")

if __name__ == '__main__':
    
    BorD = BorD_prompt()
    
    if(BorD=='benchmarks'): 
        tensorTest()
        input("\nPress any key for the next test...")
        compareProbabilities()
        input("\nPress any key for the next test...")
        timeBenchmarks()
    
    elif(BorD=='demo'):
        build = builder_prompt()
        if(build!= 'builder'):
            stop = False
            while(not stop):
                circ = Circuit(build)
                circ.run_circuit()
                esc = input("\nPress any key for another circuit or 's' to stop... ")
                if esc=="s":
                    stop = True
                else:
                    build = circuit_prompt()
        else:
            toBuild = circuit_builder_prompt()
            actual_builder(toBuild)
            #print("Mihaly code your circuit builder here, as simple as you can")

    