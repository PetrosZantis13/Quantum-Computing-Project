from abc import ABC, abstractmethod
from classtest import Matrix, MatrixElement, Vector
import numpy as np



def makesparse(matrix):
    """
    Converts dense matrix into sparse matrix in (row, column, value) form
    """
    n = matrix[0].size
    elements = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0 :
                temp = MatrixElement(i, j, matrix[i][j])
                elements.append(temp)
    return SparseMatrix(n, elements)
    
        
    

class SparseMatrix(Matrix):
    
    def __init__(self, n, elements):
        """
        Initialises the sparse matrix, assumes they are square matrices but I will change this later

        --------

        Parameters:
        n :           int
        dimension of matrix
        elements:     list or np array of MatrixElement() objects
        the requisite elements of the matrix
        """
        self.dimension = n
        self.elements = np.asarray(elements)
       
    
    def enumerator(self):
        for i in range(len(self.elements)):
                yield i

    def multiply(self, b):
        """
        Multiplies matrix with some other matrix b, will make this apply to none sparse matrices
        can be called by A*b where A is a sparse matrix
        ------------
        Parameters:
        b   :     SparseMatrix()

        Output

        p   :     SparseMatrix()
            the product of the two matrices  
        """
        assert(self.dimension == b.dimension)
        p = []
        for meb in b.elements:
            for mea in self.elements:
                if mea.j == meb.i:
                    temp = mea.val * meb.val
                    temp = MatrixElement(mea.i, meb.j, temp)
                    p.append(temp)
        p = SparseMatrix(len(p), p)
        print(p)
        return p
    
    def apply(self, v):
        """
        Applies the sparse Matrix to some vector V
        -------------
        parameters:    
        v :      Vector()
            some vector of the Vector() class

        outputs:
        u:      Vector()
            The resultant vector from applying the matrix to v

        """
        u = np.zeros(self.dimension, dtype=complex)
        for me in self.elements:
            for index in range(v.elements.size):
                if index == me.j:
                    u[me.i] += me.val * v.elements[index]
        u = Vector(u)    
        return u

    def makedense(self):
        M = np.zeros((self.dimension, self.dimension), dtype= complex)
        for me in self.elements:
            M[me.i][me.j] = me.val
        return M


    def tensorProduct(self, a):
        """
        returns the tensor product of two matrices, currently applies to two sparse matrices, will remedy this
        ------------
        parameters 
        a :      SparseMatrix()
        another sparse matrix to operate on

        output

        b :       SparseMatrix()
        result of tensor product   

        """
        
        assert (type(a) == SparseMatrix), 'Incompatible Matrices'
        elements = []
        dimension = self.dimension * a.dimension
        for me1 in self.elements:
            for mea in a.elements:
                row = me1.i*a.dimension + mea.i
                col = me1.j*a.dimension + mea.j
                value = complex(me1.val * mea.val)
                elements.append((int(row), int(col), complex(value)))
        return SparseMatrix(dimension, elements)

    def __str__(self):
        temp = ''
        for element in self.elements:
            temp += f'{element}\n'
        return temp

    


V = Vector([1,0])

mat = np.array([1,0,1,0]).reshape(2,2)

A = makesparse(mat)
B = makesparse(mat+1)

A*B