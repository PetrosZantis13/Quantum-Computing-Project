"""
Interface for the Quantum Circuit. Both implementations use this common interface for running their circuts and showing their results.
"""
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
