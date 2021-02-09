'''
Quantum Computing Project
Author: Petros Zantis

Just a test of the simulator using functions only (not OOP)
'''
import numpy as np

def state(dim, idx):
    
    state = np.zeros((dim,1))
    state[idx] = 1
    
    return state

def qubit(a, b, basis0, basis1):
    
    if(abs(a)**2 + abs(b)**2 != 1):
            print("wrong modulus")  # catch the error, maybe while loop to fix?
    
    qubit = a*basis0 + b*basis1
    return qubit

def tensor_product(inputs):
    
    product = inputs[-1]
    for i in range(len(inputs)-2,-1,-1):
        product = np.kron(inputs[i], product)
    
    return product  

def hadamard_gate():
    
    gate = np.ones((2,2))
    gate[1,1] = -1
    gate *= 1/np.sqrt(2)
    return gate

def cnot_gate():
    
    gate = np.zeros((4,4))
    gate[0,0] = 1
    gate[1,1] = 1
    gate[2,3] = 1
    gate[3,2] = 1
    return gate    
    
def Bell_state():
    
    #try to implement and check the bell states
    basis0 = state(2,0)
    basis1 = state(2,1)
    phi_plus = (np.kron(basis0, basis0) + np.kron(basis1, basis1))/(np.sqrt(2))
    print(f"\nPhi+ Bell state (Theoretical): \n{phi_plus}")
    
    control = hadamard_gate().dot(basis0)
    after = np.kron(control, basis0)
    obtained = cnot_gate().dot(after)
    print(f"\nPhi+ Bell state (Calculated): \n{obtained}")
    
def main():

    basis0 = state(2,0)
    basis1 = state(2,1)
    
    print(f"Basis state 0: \n{basis0}")
    print(f"Basis state 1: \n{basis1}")
    print(f"Orthogonality test: {basis0.T.dot(basis1) == 0}")
    
    test = (qubit(0.8, 0.6, basis0, basis1))
    
    print(f"Test qubit: \n{test}")
    tensor = tensor_product([test,test.T])
    print(f"Qubit tensor product: \n{tensor}")
    print("4 total states as expected")
    print(f"Another tensor product: \n{tensor_product([tensor, tensor.T])}")
    print("16 total states as expected\n")
    print("Now testing the Hadamard gate:")
    print(hadamard_gate())
    print("and the CNOT gate:")
    print(cnot_gate())
    
    input = tensor_product([basis1,basis0])
    print(f"\nInput state: \n{input}")
    print(f"CNOT flip: \n{cnot_gate().dot(input)}")
    
    print("\nFrom page 25 of the slides (testing the tensor product):") 
    print( tensor_product([hadamard_gate(), np.identity(2), hadamard_gate()]) )
    
    Bell_state()    
    
main()

