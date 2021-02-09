# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:54:14 2021

@author: mikva
"""
import numpy as np


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
        """
        Overwritten __str__ function

        Returns
        -------
        toPrint : string representation of register

        """
        
        toPrint = ''
        """
        for i in self.Qbits:
            toPrint += f'|0> = {i.vals[0]**2} \n'
            toPrint += f'|1> = {i.vals[1]**2} \n'
        """
        toPrint += '\n'
        for i in range(self.statevec.size):
            toPrint += f'|{i}> = {self.statevec[i]**2} \n'
        
        return toPrint
    
    def initialize(self):
        """
        Sets the statevector according to the current state of qubits

        Returns
        -------
        None.

        """
        self.statevec = np.array([1])
        for qbit in self.Qbits:
            self.statevec = np.kron(self.statevec, qbit.vals)
        
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
            self.Qbits[qbit].vals = np.array(vals[qbit]) / np.linalg.norm(vals[qbit])
        self.initialize()
        
    
class Qbit:
    def __init__(self):
        self.vals = np.array([1.+0.j, 0.+0.j])
    
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
    