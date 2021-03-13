"""
Interface for the Matrix representation.
"""

from abc import ABC, abstractmethod
import numpy as np

class MatrixElement(object): 
    """
    Gets Matrix Element .
    """
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = complex(val)
    
    def __str__(self):
        return f'{self.i}, {self.j}, {self.val}'

class Matrix(ABC):
    """
    Defines the Matrix.
    """
    
    def __init__(self, n, elements):
        self.Dimension = n
        self.Elements = elements

    def __iter__(self):
        for element in self.Elements:
            yield element
    
    @abstractmethod
    def multiply(self, m):
        pass
    
    def __mul__(self, a):
        return self.multiply(a)

    def apply(self, v):
        assert self.Dimension == v.Dimension, f'Incompatible dimensions: {self.Dimension}, {v.Dimension}'
        u = np.zeros(self.Dimension, dtype=complex)
        for me in self:
            u[me.Row] += me.Val*v[me.Col]
        return Vector(u)

class SquareMatrix(ABC):
    def __init__(self, dims):
        self.Dimension = dims
    
    def __iter__(self):
        for r in range(self.Dimension):
            for c in range(self.Dimension):
                yield MatrixElement(r,c,self[r,c])
    
    @abstractmethod
    def __getitem__():
        pass
        
    @abstractmethod
    def __setitem__():
        pass
    
    @abstractmethod
    def multiply():
        pass
    
    def apply(self, v):
        assert self.Dimension == v.Dimension, f'Incompatible dimensions: {self.Dimension}, {v.Dimension}'
        u = np.zeros(self.Dimension, dtype=complex)
        for me in self:
            u[me.Row] += me.Val*v[me.Col]
        return Vector(u)

class Vector(): 
    def __init__(self, elements):
        self.Dimension = np.array(elements).size
        self.Elements = np.array(elements, dtype=complex)
        
    def __getitem__(self, pos):
        return self.Elements[pos]
    
    def __setitem__(self, pos, val):
        self.Elements[pos] = val
    
    def outer(self, other_vec):
        """
        Returns the outer (kronecker) product of two vectors

        :param other_vec: (array) The other Vector in the multiplication
        :return: (array) The final vector product
        """
        assert type(other_vec) == Vector, 'Incompatible vector'
        dimension = self.Dimension * other_vec.Dimension
        elements = np.zeros(dimension, dtype=complex)
        for i, element in enumerate(self.Elements):
            for j, other_element in enumerate(other_vec.Elements):
                elements[i*other_vec.Dimension+j] = element * other_element
        return Vector(elements)
        
    
    def __str__(self):
        return str(self.Elements)

class explicit(Matrix):

    def __init__(self, n, elements):
        self.dimension = n
        self.elements = np.array(elements).reshape(n,n)
        

    def enumerator(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                yield MatrixElement(i, j, self.elements[i][j])
                

    def multiply(self, a, b):
        a = a.elements
        b = b.elements
        M = np.dot(a, b)
        return M

if __name__=='__main__':
    A = explicit(2,[0,1,1,1])
    
    B = explicit(2, [1,1,0,1])
    
    x = 1 + 2j
    y = 2 + 1j

