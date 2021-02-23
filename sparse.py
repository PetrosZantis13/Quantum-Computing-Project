from abc import ABC, abstractmethod
from MatrixInterface import MatrixElement, Matrix, Vector
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
        self.Dimension = n
        self.Elements = np.asarray(elements)
       
    
    def enumerator(self):
        for i in range(len(self.Elements)):
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
        assert(self.Dimension == b.Dimension)
        p = []
        for meb in b.Elements:
            for mea in self.Elements:
                if mea.j == meb.i:
                    temp = mea.val * meb.val
                    temp = MatrixElement(mea.i, meb.j, temp)
                    p.append(temp)
        p = SparseMatrix(len(p), p)
        #print(p)
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
        u = np.zeros(self.Dimension, dtype=complex)
        for me in self.Elements:
            for index in range(v.Elements.size):
                if index == me.j:
                    u[me.i] += me.val * v.Elements[index]
        u = Vector(u)    
        return u

    def makedense(self):
        M = np.zeros((self.Dimension, self.Dimension), dtype= complex)
        for me in self.Elements:
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
        dimension = self.Dimension * a.Dimension
        for me1 in self.Elements:
            for mea in a.Elements:
                row = me1.i*a.Dimension + mea.i
                col = me1.j*a.Dimension + mea.j
                value = complex(me1.val * mea.val)
                elements.append(MatrixElement(int(row), int(col), complex(value)))
        return SparseMatrix(dimension, elements)

    def __str__(self):
        temp = ''
        for element in self.Elements:
            temp += f'{element}\n'
        return temp

    

if __name__ == "__main__":
    
    V = Vector([1,0])
    
    mat = np.array([1,0,1,0]).reshape(2,2)
    
    print(mat)
    
    A = makesparse(mat)
    B = makesparse(mat+1)
    
    print(B.multiply(A))
