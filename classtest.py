from abc import ABC, abstractmethod
import numpy as np

class MatrixElement(object): 
    def __init__(self, i, j, val):
        self.i = i
        self.j = j
        self.val = val

class Matrix(ABC): 
    
    def __init__(self, n):
        self.dimension = n
        #m = self.matrix
        super(Matrix, self).__init__()

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
    
    def __mul__(a, b):
        return a.multiply(b)


    def apply(self, v): #trying to figure out how to get this to work
        assert(dimension == v.dimension, "Incompatible dimensions")
        u = Vector(dimension)
        for element in self:
            element = MatrixElement()

        return u








class explicit(Matrix):

    def __init__(self, n):
        super().__init__(n)
        self = np.zeros((n,n))
        

    def enumerator(self):
        for i in self:
            for j in i:
                yield MatrixElement(i, j, self[i][j])

    def multiply(self, m):
        M = np.dot(self, m)
        return M

A = explicit(2)

B = explicit(2)

