# Singular-value decomposition

'''
Where A is the real m x n matrix that we wish to decompose,
U is an m x m matrix, Sigma (often represented by the
uppercase Greek letter Sigma) is an m x n diagonal matrix,
and V^T is the  transpose of an n x n matrix where T is a
superscript.
'''

from numpy import array, diag, zeros, dot
from scipy.linalg import svd
# define a matrix
A = array([[1, 2], [3, 4], [7, 8],[5, 6]])
print("A:",A.shape, A)
# SVD
U, s, VT = svd(A)
# create m x n Sigma matrix
Sigma = zeros((A.shape[0], A.shape[1]))
# populate Sigma with n x n diagonal matrix
Sigma[:A.shape[1], :A.shape[1]] = diag(s)
print("U:",U.shape,U)
print("Sigma:",Sigma.shape,Sigma)
print("VT:",VT.shape,VT)

B = U.dot(Sigma.dot(VT))
print(B)
