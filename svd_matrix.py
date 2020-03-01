# Singular-value decomposition
#Reference: https://machinelearningmastery.com/singular-value-decomposition-for-machine-learning/
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
A = array([
	[1,2,3,4,5,6,7,8,9,10],
	[11,12,13,14,15,16,17,18,19,20],
	[21,22,23,24,25,26,27,28,29,30]])
print("A:",A.shape, A)
# SVD
U, s, VT = svd(A)
print(s)
# create m x n Sigma matrix
Sigma = zeros((A.shape[0], A.shape[1]))
# populate Sigma with n x n diagonal matrix
Sigma = diag(s)

#dimensionality reduction of Sigma - keep only 2 columns
print("Old sigma:",Sigma.shape,Sigma)

Sigma = Sigma[:, :2]

print("U:",U.shape,U)
print("New sigma:",Sigma.shape,Sigma)
print("VT:",VT.shape,VT)

B = U.dot(Sigma.dot(VT))
print(B)
