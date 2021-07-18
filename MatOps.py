from Float import FloatNum

class FloatMatrix:
    def __init__(self,X) -> None:
        self.X = X
        self.rows = len(X)
        self.columns = len(X[0])
        if(not all(len(i)==self.columns for i in X)):
            raise(Exception('Non uniform colums not allowed in matrix'))

    def mat_add(self,Y):
        if(len(self.X) != len(Y.X)):
            raise(Exception('Incompatible sizes'))

        Z = [[None]*self.columns for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.columns):
                Z[i][j] = self.X[i][j]+Y.X[i][j]

        return(Z)

    def mat_dot_product(self,Y):
        if(len(self.X) != len(Y.X)):
            raise(Exception('Incompatible sizes'))

        Z = None

        for i in range(self.rows):
            for j in range(self.columns):
                if(Z==None):
                    Z = self.X[i][j]*Y.X[i][j]
                else:
                    Z = Z + self.X[i][j]*Y.X[i][j]

        return(Z)

    def mat_mul(self,Y):
        if(self.columns != Y.rows):
            raise(Exception('Incompatible sizes'))

        Z = [[None]*Y.columns for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(Y.columns):
                for k in range(self.columns):
                    if(Z[i][j] == None):
                        Z[i][j] = self.X[i][k] * Y.X[k][j]
                    else:
                        Z[i][j] = Z[i][j] + (self.X[i][k] * Y.X[k][j])

        return(Z)

    def max_pool(self):
        max = self.X[0][0]
        for i in self.X:
            for j in i:
                if(j>max):
                    max = j
        return max

    def print_matrix(self):
        for i in self.X:
            for j in i:
                j.show_num()
                print(end='\t')
            print()

def to_float_matrix(X,exp_bits=8,man_bits=23):
    return([[FloatNum(j,exp_bits=exp_bits,man_bits=man_bits) for j in i] for i in X])    

X = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]


Y = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
# X=to_float_matrix(X,8,23)
# Y=to_float_matrix(Y,8,23)
# X = FloatMatrix(X)
# Y = FloatMatrix(Y)

# Z = X.mat_add(Y)
# Z = FloatMatrix(Z)
# Z.print_matrix()

# print()

# Z = X.mat_mul(Y)
# Z = FloatMatrix(Z)
# Z.print_matrix()

# print()

# Z = X.mat_dot_product(Y)
# print(Z)

# print(X.max_pool())