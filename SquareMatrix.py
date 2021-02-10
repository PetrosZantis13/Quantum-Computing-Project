# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:15:18 2021

@author: mikva
"""
import numpy as np

def toSparse(matrix):
    assert type(matrix)==np.ndarray, 'Matrix not of type np.ndarray'
    assert matrix[0].size**2 == matrix.size, 'Matrix is not square'
    elements = []
    dimension = matrix[0].size
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j] != 0:
                elements.append((int(i),int(j),matrix[i][j]))
    return SparseMatrix(dimension, elements)
    

class SparseMatrix():
    def __init__(self, dimension, elements):
        #Attention! must ensure row and column values are given as int!
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
        
    def tensorProd(self, other_matrix):
        """
        Tensor product product of two sparse matrices.

        Parameters
        ----------
        other_matrix : Sparse_Matrix
            The matrix to be multiplied by

        Returns
        -------
        Sparse_Matrix
            The tensor product of the two matrices in the form of self (x) other_matrix
        """
        assert (type(other_matrix) == SparseMatrix), 'Incompatible Matrices'
        elements = []
        dimension = self.Dimension * other_matrix.Dimension
        for i in self.Elements:
            for j in other_matrix.Elements:
                row = i[0]*other_matrix.Dimension + j[0]
                col = i[1]*other_matrix.Dimension + j[1]
                value = i[2] * j[2]
                elements.append((int(row), int(col), value))
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
        u = np.zeros(self.Dimension, dtype=complex)
        for me in self.Elements: 
            u[int(me[0])] += me[2] * vector.Elements[int(me[1])]
        return Vector(u)
    
    def show(self):
        """
        Prints the entire matrix onto the console for visualisation purposes.
        Only advised up to 16x16 matrices

        Returns
        -------
        None.
        """
        matrix = np.zeros((self.Dimension, self.Dimension))
        for element in self.Elements:
            matrix[element[0]][element[1]] = element[2]
        print(matrix)
        
    def toDense(self):
        """
        Dense representation of the matrix.

        Returns
        -------
        matrix : nd.array
            Dense representation of the matrix.
        """
        matrix = np.zeros((self.Dimension, self.Dimension))
        for element in self.Elements:
            matrix[element[0]][element[1]] = element[2]
        return matrix
    
    def __str__(self):
        toPrint = ''
        for element in self.Elements:
            toPrint += f'({element[0]}, {element[1]}, {element[2]})\n'
        return toPrint

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
        assert type(other_vec) == Vector, 'Incompatible vector'
        dimension = self.Dimension * other_vec.Dimension
        elements = np.zeros(dimension, dtype=complex)
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
    """
    #mat2 = SparseMatrix(4, [(0,0,1), (1,1,1), (2,2,1), (3,3,1)])
    #mat1 = SparseMatrix(4, [(0,3,1), (1,2,1), (2,1,1), (3,0,1)])
    mat1 = SparseMatrix(2, [(0,1,1), (1,0,1)])
    mat2 = SparseMatrix(2, [(0,0,1), (1,1,1)])
    bigmat = mat1.tensorProd(mat2)
    evenbiggermat = bigmat.tensorProd(mat1)
    
    vec1 = Vector(np.array([0,1]))
    vec2 = Vector(np.array([1,0]))
    vec3 = vec1.outer(vec2)
    #vec4 = mat1.Apply(vec3)
    print(vec1)
    print(vec2)
    print(vec3)
    print(vec4)
    
    print(mat1)
    mat1.show()
    print(bigmat)
    bigmat.show()
    print(evenbiggermat)
    evenbiggermat.show()
    """