
from MatrixInterface import MatrixElement, Matrix, Vector, SquareMatrix
import numpy as np
# Test
def makeSparse(matrix):
    """
    Converts dense matrix into sparse matrix in (row, column, value) form
    
    :param matrix: (list) Matrix to be converted to Sparse
    :return: (list) Sparse matrix
    """
    n = matrix[0].size
    elements = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0 :
                temp = MatrixElement(i, j, matrix[i][j])
                elements.append(temp)
    return SparseMatrix(n, elements)
    
class ColumnElement():
    """
    Column element ina sparse matrix
    """
    def __init__(self, j, val):
        self.Row = j
        self.Val = complex(val)
    

class SparseMatrix(Matrix, object):
    """
    Creates sparse matrix, assumes they are square matrices 
    
    :param n: (int) dimensions of matrix
    :param elements: (list) objects the requisite elements of the matrix

    """
    
    def __init__(self, n, elements):
        super().__init__(n, elements)

    def multiply(self, b):
        """
        Multiplies matrix with some other matrix b, will make this apply to none sparse matrices
        can be called by A*b where A is a sparse matrix

        :param b: SparseMatrix()
        :return: (list) the product of two matrices
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

        :param v: some vector of the Vector() class
        :return: (list) The resultant vector from applying the matrix to v
        """
        u = np.zeros(self.Dimension, dtype=complex)
        for me in self.Elements:
            for index in range(v.Elements.size):
                if index == me.j:
                    u[me.i] += me.val * v.Elements[index]
        u = Vector(u)    
        return u

    def makedense(self):
        """makes a dense matrix"""
        M = np.zeros((self.Dimension, self.Dimension), dtype= complex)
        for me in self.Elements:
            M[me.i][me.j] = me.val
        return M


    def tensorProduct(self, a):
        """
        Returns the tensor product of two matrices, 
        currently applies to two sparse matrices

        :param a: (list) sparse matrix to operate on
        :return: (list) result of tensor product

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

class ColMatrix(SquareMatrix):
    """
    A type of sparse matrix extending the Square Matrix class
    """
    def __init__(self, dims):
        """
        Constructor
        :param dims: (int) dimension of the matrix
        """
        super().__init__(dims)
        self.Columns = [[] for i in range(dims)]
    
    def __setitem__(self, pos, val):
        """
        Sets a specific item in the matrix

        :param pos: (tuple) Position of the item to be set
        :param val: (complex) Value to set the item to
        """
        row, col = pos
        if len(self.Columns[col])==0:
            self.Columns[col].append(ColumnElement(row, val))
        
        elif self.Columns[col][-1].Row < row:
            self.Columns[col].append(ColumnElement(row, val))
        
        else:
            for index, element in enumerate(self.Columns[col]):
                if element.Row == row:
                    self.Columns[col][index] = ColumnElement(row, val)
                    break
                elif element.Row >= row:
                    self.Columns.insert(index-1, ColumnElement(row, val))
                    break
                
    def __getitem__(self, pos):
        """
        Gets a specific item from the matrix

        :param pos: (tuple) Position of the item to acquire
        :return: (complex) number at that position in the matrix
        """
        row, col = pos
        if len(self.Columns[col])==0:
            return complex(0)
        for element in self.Columns[col]:
            if element.Row == row: return element.Val
            if element.Row >= row: return complex(0)
        return complex(0)
        
    def __str__(self):
        toPrint = ''
        #i = 0
        for c, column in enumerate(self.Columns):
            #print(column)
            for element in column:
                
                #i+=1
                toPrint += f'{element.Row}, {c}, {element.Val} \n'
        return toPrint
        
    def __iter__(self):
        for col, column in enumerate(self.Columns):
            for element in column:
                yield MatrixElement(element.Row, col, element.Val)
    
    def tensorProduct(self, otherMatrix):
        """
        Calculates the tensor product of two Column Matrices.
        
        :param otherMatrix: (ColMatrix) the matrix on the right hand side of the tensor product
        :return newMatrix: (ColMatrix) new matrix representing the tensor product
        """
        newMatrix = ColMatrix(self.Dimension*otherMatrix.Dimension)
        for col1, column in enumerate(self.Columns):
            for element in column:
                for col2, othercolumn in enumerate(otherMatrix.Columns):
                    for otherElement in othercolumn:
                        #print(row1, row2, element.Col, otherElement.Col)
                        #print(row1*otherMatrix.Dimension+row2, element.Col*otherMatrix.Dimension + otherElement.Col)
                        newMatrix[element.Row*otherMatrix.Dimension+otherElement.Row, col1*otherMatrix.Dimension + col2] = element.Val*otherElement.Val
        return newMatrix
        
    def toDense(self):
        """
        Creates a dense numpy matrix representation of the matrix

        :return dense: (numpy.ndarray) Numpy array representing the matrix
        """
        dense = np.zeros((self.Dimension, self.Dimension), dtype=complex)
        for col, column in enumerate(self.Columns):
            for element in column:
                dense[element.Row, col] = element.Val
        return dense
    
    def multiply(self, m):
        """
        Multiplies self with another matrix

        :param m: (ColMatrix) other matriix on the right hand side of the multiplication
        :return p: (ColMatrix) Product of the multiplication
        """
        p = ColMatrix(self.Dimension)
        for me in m:
            column = self.Columns[me.Row]
            for ce in column:
                p[ce.Row, me.Col] += ce.Val*me.Val
        return p
    
class LazyMatrix(SquareMatrix):
    """
    Creates a lazy matrix
    """
    def __init__(self, dims):
        """
        Initialiser

        :param dims: (int) dimension of the matrix
        """
        super().__init__(dims)
        self.Cache = None
        
    def multiply(self, m):
        """
        This operation is useless in our case and doesn't actually work, so ... yeah

        :param m: (LazyMatrix) matrix to multiply by (perhaps implemented in the future)
        :return None:
        """
        assert self.Dimension == m.Dimension, 'Incompatible dimensions'
        print('this operation is useless in our case')
        return None
        return LazyMatrix(self.Dimension, lambda v: self.apply(m.apply(v)))
    
    def __getitem__(self, pos):
        if len(self.Cache)==0:
            self.Evaluate()
        return self.Cache[pos]
        
    def __setitem__(self, pos, val):
        print('cannot set elemtent of lazymatrix')
        #return None
    
    def Evaluate(self):
        """
        Evaluates the entire matrix, not recommended to ever call it. Takes a long time and is useless for our purposes
        Puts the evaluated ColMatrix into self.Cache
        """
        cache = ColMatrix(self.Dimension)
        for col in range(self.Dimension):
            basisElement = Vector(np.zeros(self.Dimension))
            basisElement[col] = 1
            column = self.apply(basisElement)
            for row in range(self.Dimension):
                cache[row, col] = column[row]
        self.Cache = cache
        
    def __str__(self):
        if self.Cache==None:
            self.Evaluate()
        return self.Cache.__str__()
        
class Gate(LazyMatrix):
    """
    Lazy representation of a quantum gate
    """
    def __init__(self, dims, sm, qbpos):
        """
        Initialises Gate

        :param dims: (int) dimensions of the large gate
        :param sm: (ColMatrix) The sparse matrix representing the quantum gate
        :param qbpos: (list) The qubits which the gate is applied to
        """
        super().__init__(dims)
        self.SM = sm
        self.smDim = sm.Dimension
        self.qbpos = np.array(qbpos)
    
    def apply(self, v):
        """
        Applies the Gate to a vector

        :param v: (array or Vector) The vector the gate will be applied to, must be the same dimesion as self
        :return w: (Vector) The result of the application of the gate
        """
        w = Vector(np.zeros(self.Dimension))
        for i in range(self.Dimension):
            r = self.__gather(i)
            i0 = i & ~self.__scatter(r)
            for c in range(self.smDim):
                j = i0 | self.__scatter(c)
                w[i] += self.SM[r,c] * v[j]
        return w
        
    def __gather(self, i):
        """
        Magic method that I do not completely understand

        :param i: (int) The row number of the gate
        :return j: (int)
        """
        j = 0
        for k in range(len(self.qbpos)):
            j |= ((i >> self.qbpos[k]) & 1) << k
        return j
    
    def __scatter(self, j):
        """
        Magic method that I do not completely understand

        :param i: (int)
        :return j: (int)
        """
        i = 0
        for k in range(len(self.qbpos)):
            i |= ((j>>k)&1) << self.qbpos[k]
        return i


def toColMat(mat):
    """
    Creates a ColMatrix representation from an numpy array

    :param mat: (numpy.ndarray) Array to be converted
    :return toReturn: (ColMatrix) Column matrix representation of mat
    """
    mat = np.array(mat, dtype=complex)
    toReturn = ColMatrix(mat[0].size)
    for i in range(mat[0].size):
        for j in range(mat[0].size):
            
            if mat[i,j] != 0: toReturn[i,j] = mat[i,j]
    return toReturn

if __name__ == "__main__":
    pass
