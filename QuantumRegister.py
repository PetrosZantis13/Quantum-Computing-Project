# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:54:14 2021

@author: mikva
"""
import numpy as np
import SquareMatrix as sm


class QuantumRegister:
    def __init__(self, n):
        """
        Initializes the quantum register of length n. Creates a list of default qubits
        in state |0> and initializes the wavevector which describes the register

        Parameters
        ----------
        n : int
            length of register

        Returns
        -------
        None.

        """
        Qbits = []

        for i in range(n): 
            Qbits.append(Qbit())
        self.Qbits = np.array(Qbits)
        self.initialize()        

    def __str__(self):        
        toPrint = ''

        toPrint += '\n'
        for i in range(self.Statevec.Elements.size):
            toPrint += f'|{i}> = {self.Statevec.Elements[i]**2} \n'
        
        return toPrint
    
    def initialize(self):
        """
        Sets the statevector according to the current state of qubits

        Returns
        -------
        None.

        """
        self.Statevec = sm.Vector(np.array([1]))
        for qbit in self.Qbits:
            self.Statevec = self.Statevec.outer(qbit.vals)
        
    def setQbits(self, qbits, vals):
        """
        Sets the initial values of the qubits if required,
        although it is preferred to use gates for this step.
        Automatically normalizes the Qbit

        Parameters
        ----------
        qbits : array_like
            qubits to be set
        vals : array_like, each entry containing two values
            The values that the qubits should be set to.

        Returns
        -------
        None.

        """
        
        for qbit in qbits:
            self.Qbits[qbit].vals.Elements = np.array(vals[qbit]) / np.linalg.norm(vals[qbit])
        self.initialize()
        
    
class Qbit:
    def __init__(self):
        self.vals = sm.Vector(np.array([1.+0.j, 0.+0.j]))
    
    def get0(self):
        return self.vals[0]
    
    def get1(self):
        return self.vals[1]
    
    def __str__(self):
        toPrint = ''
        toPrint += f'|0> = {self.vals[0]} \n'
        toPrint += f'|1> = {self.vals[1]} \n'
        
        return toPrint
        

if __name__ == '__main__':
    pass
    