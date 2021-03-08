# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 19:15:57 2021

@author: mikva
"""
from abc import ABC, abstractmethod

class InterfaceClass(ABC):
    def __init__(self, name, size):
        self.Size = size
        self.Name = name
        
    def __str__(self):
        toString = self.Name + f', a {self.Size} qubit big quantum circuit'
        return toString
    
    @abstractmethod
    def simulate():
        pass
    
    @abstractmethod
    def return_measurements():
        pass
    
    @abstractmethod
    def show():
        pass