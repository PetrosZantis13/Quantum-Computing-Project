# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:15:18 2021

@author: mikva
"""
import numpy as np
#from enum import Enum

"""
class Matrix_Element(Enum):
    def __init__(self, row, col, value):
        self.Row = row
        self.Col = col
        self.Val = value
"""

class SparseMatrix():
    def __init__(self, dimension, elements):
        """
        Initializes the sparse matrix

        Parameters
        ----------
        dimension : int
            number of dimensions of the matrix
        elements : tuple
            one matrix element of the sparse matrix. Must be of the form (row, column, value)

        Returns
        -------
        None.

        """
        self.Dimension = dimension
        self.Elements = np.array(elements)
        
    def outer(self, other_matrix):
        """
        Outer (Kronecker) product of two sparse matrices.

        Parameters
        ----------
        other_matrix : Sparse_Matrix
            The matrix to be multiplied by

        Returns
        -------
        Sparse_Matrix
            The outer product of the two matrices.

        """
        assert (type(other_matrix) == SparseMatrix), 'Incompatible Matrices'
        elements = []
        dimension = self.Dimension * other_matrix.Dimension
        for i in self.Elements:
            for j in other_matrix.Elements:
                row = i[0]*other_matrix.Dimension + j[0]
                col = i[1]*other_matrix.Dimension + j[1]
                value = i[2] * j[2]
                elements.append((row, col, value))
        return SparseMatrix(dimension, elements)
    
    def Apply(self, vector):
        """
        Applies the matrix to the vector specified and returns the new vector.

        Parameters
        ----------
        vector : Vector
            The wavevector describing the system.

        Returns
        -------
        Vector
            The new statevector after the matrix is applied
        """
        assert (self.Dimension == vector.Dimension), 'Incompatible dimensions'
        u = np.zeros(self.Dimension)
        for me in self.Elements: u[me[0]] += me[2] * vector.Elements[me[1]]
        return Vector(u)

"""
class SquareMatrix():
    def __init__(self, dimension, elements): 
        self.Dimension = dimension
        self.Elements = np.array(elements)
    # implement enumerator thingys
    def Complex(self, row, col): pass
    
    def Multiply(self, m): pass
    def Apply(self, v):
        assert (self.Dimension == v.size), 'Incopatible dimensions'
        u = np.zeros(self.Dimension)
        for me in self.Elements: u[me.row] += me.val * v[me.col]
        return u
    
class SparseMatrix(SquareMatrix):
    def __init__(self, dimension, elements):
        super(dimension, elements)
        self.columns = []
        for i in range(self.Dimension): self.columns.append([])
        
    
    def Multiply(self, m):
        assert (self.Dimension == m.size), 'Incopatible dimensions'
        p = SquareMatrix()
        for me in m.elements:
            column = self.columns[me[0]]
            for ce in column: p[ce[0], me[1]] += ce[2] * me[2]
        return p
"""

class Vector():
    def __init__(self, elements):
        self.Dimension = elements.size
        self.Elements = np.array(elements)
    
    def outer(self, other_vec):
        """
        Returns the outer (kronecker) product of two vectors

        Parameters
        ----------
        other_vec : Vector
            The other Vector in the multiplication

        Returns
        -------
        Vector
            The final vector product

        """
        assert type(other_vec == Vector), 'Incompatible vector'
        dimension = self.Dimension * other_vec.Dimension
        elements = np.zeros(dimension)
        for i, element in enumerate(self.Elements):
            for j, other_element in enumerate(other_vec.Elements):
                elements[i*other_vec.Dimension+j] = element * other_element
        return Vector(elements)
    
    def __str__(self):
        toPrint = ''
        for i in self.Elements:
            toPrint += f'{i} '
        return toPrint

if __name__ == '__main__':
    #sp = SparseMatrix(4, [(0,0,1), (1,1,1), (2,2,1), (3,3,1)])
    mat1 = SparseMatrix(4, [(0,3,1), (1,2,1), (2,1,1), (3,0,1)])
    vec1 = Vector(np.array([0,1]))
    vec2 = Vector(np.array([1,0]))
    vec3 = vec1.outer(vec2)
    vec4 = mat1.Apply(vec3)
    print(vec1)
    print(vec2)
    print(vec3)
    print(vec4)