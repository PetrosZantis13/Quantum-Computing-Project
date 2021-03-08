'''
Quantum Computing Project 
Author: Petros Zantis
'''
from abc import ABC, abstractmethod

class Interface(ABC):
    
    @abstractmethod
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def run_circuit(self):
        pass
    
    @abstractmethod
    def show_results(self):
        pass
    
    '''
    Mihaly you can ignore this, I just had these prompts
    so that the user can select the size of the system etc
    
    @abstractmethod
    def size_prompt(self):
        pass
 
    @abstractmethod
    def qubit_prompt(self):
        pass
    '''