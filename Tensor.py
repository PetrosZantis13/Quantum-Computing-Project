'''
The Tensor Module is used to represent registers or parallel gates in a circuit.
The reason is that these structures comprise of tensor products of qubits or 
gates respectively. 
'''
import numpy as np
import State
import Gate

class Tensor(object):
    """
    Calculates Tensor Product

    :param inputs: (list) Matrix to calculate the Tensor Product.

    """

    def __init__(self, inputs) :        

        assert isinstance(inputs, list), "Inputs must be a list"    
        self.inputs = inputs   
        
    def calculate(self):   
        '''Calculates the outer product of the inputs from right to left, 
        since that is the order of applying them in Linear Algebra, and saves
        the product in matrix form as its attribute. This method allows for
        the object to recalculate the outer product, for 
        example when any of the qubits from the register are collapsed.
        '''
        
        if(all(isinstance(state, State.State) for state in self.inputs)):
            # Tensor product of states
            product = self.inputs[-1].vector
            for i in range(len(self.inputs)-2,-1,-1):
                product = np.kron(self.inputs[i].vector, product)
                
        elif(all(isinstance(gate, Gate.Gate) for gate in self.inputs)):
            # Tensor product of gates
            product = self.inputs[-1].operator
            for i in range(len(self.inputs)-2,-1,-1):
                product = np.kron(self.inputs[i].operator, product)
        else:
            print("Incompatible inputs!")
            
        self.product = product
    
    def to_gate(self, gate_name):
        """Converts the tensor product to a Gate object.

        :param gate_name: (str) Name of the Gate 
        :return: gate as it is constructed
        """
        
        self.calculate()        
        gate = Gate.Gate(gate_name)
        gate.build_gate(self.product)
        return gate
    
    def to_state(self):
        """Converts the tensor product to a State object.

        :return: state as it is constructed
        """
        self.calculate()        
        state = State.State(self.product)
        return state