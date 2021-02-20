from abc import ABC, abstractmethod
import numpy as np

class MatrixElement(object): 
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = complex(val)
    
    def __str__(self):
        return f'{self.i}, {self.j}, {self.val}'

class Matrix(ABC): #Matrix interface, will implement this better

    
    def __init__(self, n, elements):
        self.dimension = n
        self.elements = elements

    #@abstractmethod
    def get_value(self, i, j):
        pass

    #@abstractmethod
    def set_value(self):
        pass

    def enumerator(self):
        for i in range(0, dimension):
            for j in range(0, dimension):
                yield MatrixElement(i,j, get_value(i,j))
    
    @abstractmethod
    def multiply(self, m):
        pass
    
    def __mul__(self, a):
        return self.multiply(a)


    def apply(self, v): 
        pass

class Vector(): #copied from mihaly
    def __init__(self, elements):
        self.dimension = np.array(elements).size
        self.elements = np.array(elements, dtype=complex)
    
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
        assert type(other_vec) == Vector, 'Incompatible vector'
        dimension = self.Dimension * other_vec.Dimension
        elements = np.zeros(dimension, dtype=complex)
        for i, element in enumerate(self.elements):
            for j, other_element in enumerate(other_vec.elements):
                elements[i*other_vec.Dimension+j] = element * other_element
        return Vector(elements)
        
    
    def __str__(self):
        toPrint = ''
        for i in self.elements:
            toPrint += f'{i} '
        return toPrint






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

A = explicit(2,[0,1,1,1])

B = explicit(2, [1,1,0,1])

x = 1 + 2j
y = 2 + 1j

