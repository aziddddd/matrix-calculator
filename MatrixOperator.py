import random

class MatrixError(Exception):
    """ An exception class for Matrix """
    pass

class MyMatrix(object):
    """
    Class to create a matrix and run basic operations.
    
    Properties:
    rows(list) - rows of matrix
    m(integer) - no. of rows
    n(integer) - no. of columns
    
    Methods:
    * formatted output
    * addition
    * subtraction
    * multiplication
    * get inverse matrix
    * get random matrix
    * get zero matrix
    * get identity matrix
    """

    def __init__(self, m, n, zero=True):
        """
        Initialise a Matrix instance

        :arg zero:  *True  - Create a known dimension matrix with elements of zero (Zero Matrix)
                    *False - Create a known dimension matrix with no elements          
        :param m: no. of rows as integer
        :param n: no. of columns as integer    
        :param rows: each rows as element of a list
        """

        if zero:
            self.rows = [[0]*n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n

    def __str__(self):
        """
        Define output format.
        This will print the matrix itself row by row.
        i.e. For a 2 by 3 matrix, it will print
                1 2 3
                4 5 6
        """

        s = '\n'.join([' '.join([str(item) for item in row]) for row in self.rows])
        return s + '\n'

    def __getitem__(self, idx):
        """ Return the element of a row of matrix """

        return self.rows[idx]

    def __setitem__(self, idx, item):
        """ Set item as the element of a row of matrix """
        
        self.rows[idx] = item


    def getdeter(self, minor, deterlist):
        """ Find inner determinants to calculate determinant of the matrix """

        if minor.m == 2:
            determinant = (minor.rows[0][0]*minor.rows[1][1])-(minor.rows[0][1]*minor.rows[1][0])
            return determinant
        else:
            deterlist['self : {} minor: {}'.format(self.m, minor.m)] = []
            row = 0
            for col in range(minor.n):
                innerminor_row = minor.getMinor(row, col)
                innerminor = MyMatrix(minor.m-1, minor.n-1, False)
                innerminor.rows = innerminor_row
                deterlist['self : {} minor: {}'.format(self.m, minor.m)].append((-1)**(row+col) * minor.rows[row][col] * minor.getdeter(innerminor, deterlist))            
            return sum(deterlist['self : {} minor: {}'.format(self.m, minor.m)])

    def getDeterminant(self, deterlist):
        """ Return a determinant of the matrix """
        if len(deterlist) == 0:
            deterlist['inner'] = []
        row = 0
        for col in range(self.n):
            check = False
            minor_row = self.getMinor(row, col)
            minor = MyMatrix(self.m-1, self.n-1, False)
            minor.rows = minor_row
            sub_sub_deter = self.getdeter(minor,deterlist)
            sub_deter = (-1)**(row+col) * self.rows[row][col]*sub_sub_deter
            deterlist['inner'].append(sub_deter)
        return sum(deterlist['inner'])

    def getCofactor(self, deterlist2, finalise=True):       
        """ Return a cofactor of the matrix """
 
        cofactorRows = []
        for row in range(self.m):
            cofactorRow = []
            for col in range(self.n):
                minor_row = self.getMinor(row, col)
                minor = MyMatrix(self.m-1, self.n-1, False)
                minor.rows = minor_row
                if finalise:
                    cofactorRow.append(((-1)**(row+col)) * self.getdeter(minor, deterlist2))
                else:
                    deter = self.getdeter(minor, deterlist2)
            cofactorRows.append(cofactorRow)
        cofactor = MyMatrix(self.m, self.n, False)
        cofactor.rows = cofactorRows

        return cofactor

    def getMinor(self, i, j):
        return [row[:j] + row[j+1:] for row in (self.rows[:i]+self.rows[i+1:])]

    def getInverse(self):
        """ Return a inverse of the matrix """
        if self.m != self.n:
            raise MatrixError('Non-square matrices has no inverse!')

        deterlist = {}
        determinant = self.getDeterminant(deterlist)

        if determinant == 0:
            raise MatrixError('Determinant is zero. The matrix has no inverse!')

        if self.m == self.n == 2:
            inv = MyMatrix(self.m, self.n, False)
            inv.rows.append([1/determinant*self.rows[1][1], 1/determinant*-1*self.rows[0][1]])
            inv.rows.append([1/determinant*-1*self.rows[1][1], 1/determinant*self.rows[0][0]])
            return inv

        deterlist2 = {}
        cofactor = self.getCofactor(deterlist2)
        adjmat = cofactor.getTranspose()
        inv = MyMatrix(self.m, self.n, False)
        for index, y in enumerate(adjmat.rows):
            inv.rows.append([])
            for z in y:
                inv.rows[index].append(z/determinant)
        return inv
        

    def getTranspose(self):
        """ Return a transpose of the matrix """
        
        m, n = self.n, self.m
        mat = MyMatrix(m, n)
        mat.rows =  [list(item) for item in zip(*self.rows)]  

        return mat

    def getRank(self):
        """ Return a tuple of no. of rows and columns """

        return (self.m, self.n)

    def __add__(self, mat):
        """ Add a matrix to this matrix """
        
        if self.getRank() != mat.getRank():
            raise MatrixError('Trying to add matrixes of varying rank!')


        ret = MyMatrix(self.m, self.n)
        
        for x in range(self.m):
            row = [sum(item) for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __sub__(self, mat):
        """ Subtract a matrix from this matrix """
        
        if self.getRank() != mat.getRank():
            raise MatrixError('Trying to add matrixes of varying rank!')


        ret = MyMatrix(self.m, self.n)
        
        for x in range(self.m):
            row = [item[0]-item[1] for item in zip(self.rows[x], mat[x])]
            ret[x] = row

        return ret

    def __mul__(self, mat):
        """ Multiply a matrix with this matrix """
        
        matm, matn = mat.getRank()
        if (self.n != matm):
            raise MatrixError("Matrices cannot be multipled!")
        
        mat_t = mat.getTranspose()
        mulmat = MyMatrix(self.m, matn)
        
        for x in range(self.m):
            for y in range(mat_t.m):
                mulmat[x][y] = sum([item[0]*item[1] for item in zip(self.rows[x], mat_t[y])])

        return mulmat

    @classmethod
    def makeRandom(cls, m, n, low=0, high=5):
        """ Make a random matrix with elements in range (low-high) """
        
        obj = MyMatrix(m, n, zero=False)
        for x in range(m):
            obj.rows.append([random.randrange(low, high) for i in range(obj.n)])

        return obj

    @classmethod
    def makeId(cls, m):
        """ Make identity matrix of rank (mxm) """

        rows = [[0]*m for x in range(m)]
        n = len(rows[0])
        idx = 0
        for row in rows:
            row[idx] = 1
            idx += 1
            
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise MatrixError("inconsistent row length")
        mat = MyMatrix(m, n, zero=False)
        mat.rows = rows

        return mat