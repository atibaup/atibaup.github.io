import numpy as np
from numpy import linalg as la
from matplotlib import pyplot as plt

n = 200 # matrix size
rank = 2
k = 2

def minNonZeroEigVal(Z, k):
	l = la.eigvalsh(Z)
	return l[np.argsort(l)][k]

def minEigVal(Z):
	return np.min(la.eigvalsh(Z))

def maxEigVal(Z):
	return np.max(la.eigvalsh(Z))

def sortedEig(Z):
	(l, v) = la.eig(Z)
	indx = np.argsort(l)
	return (l[indx], v[:, indx])

nRndm = 10
nFs = 10

minEigA = np.empty((nRndm, nFs))
minEigB1 = np.empty((nRndm, nFs))
minEigB2 = np.empty((nRndm, nFs))
maxEigA = np.empty((nRndm, nFs))
maxEigB1 = np.empty((nRndm, nFs))
maxEigB2 = np.empty((nRndm, nFs))
condA = np.empty((nRndm, nFs))
condB = np.empty((nRndm, nFs))
lBound = np.empty((nRndm, nFs))
uBound = np.empty((nRndm, nFs))

f_s = np.linspace(1, 2, nFs)
for (i, f) in enumerate(f_s):
	print "f=%f" % f
	for r in xrange(nRndm):
		X = 1.0 / np.sqrt(n) * np.random.randn(int(f * n), n)

		A = np.dot(X.T, X)

		(lambda_, V) = sortedEig(A)

		U1 = np.dot(V[:, 0:k], np.random.randn(k, rank))

		B1 = A + np.dot(U1, U1.T)

		U2 = np.dot(V[:, k:n], np.random.randn(n - k, rank))

		B2 = A + np.dot(U2, U2.T)

		minEigA[r, i] = lambda_[0]
		minEigB1[r, i] = minEigVal(B1)
		minEigB2[r, i] = minEigVal(B2)
		lBound[r, i] = min((lambda_[0] + minNonZeroEigVal(np.dot(U1, U1.T), n - k), lambda_[k]))
		uBound[r, i] = max((lambda_[k-1] + minNonZeroEigVal(np.dot(U1, U1.T), n-1), lambda_[n-1]))
		maxEigA[r, i] = maxEigVal(A)
		maxEigB1[r, i] = maxEigVal(B1)
		maxEigB2[r, i] = maxEigVal(B2)
		condA[r, i] = lambda_[n-1] / lambda_[0]
		condB[r, i] = maxEigB1[r, i] / minEigB1[r, i] 

		if (minEigB1[r, i] < minEigA[r, i]):
			print "Error %f (minEigB1) < %f (minEigA)" % (minEigB1[r, i], minEigA[r, i])

		if (minEigB1[r, i] < lBound[r, i]):
			print "Error %f (minEigB1) < %f (bound)" % (minEigB1[r, i], lBound[r, i])

avgMinEigA = np.mean(minEigA, axis = 0)
avgMinEigB1 = np.mean(minEigB1, axis = 0)
avgMinEigB2 = np.mean(minEigB2, axis = 0)

avgMaxEigA = np.mean(maxEigA, axis = 0)
avgMaxEigB1 = np.mean(maxEigB1, axis = 0)
avgMaxEigB2 = np.mean(maxEigB2, axis = 0)

avgCondA = np.mean(condA, axis = 0)
avgCondB = np.mean(condB, axis = 0)

(fig, axs) = plt.subplots(3, 1)
axs[0].semilogy(f_s, avgMinEigA, '-r')
axs[0].semilogy(f_s, avgMinEigB1, '-b')
#plt.semilogy(f_s, avgMinEigB2, '--b')
axs[0].semilogy(f_s, np.mean(lBound, axis =0), '--b')

axs[0].legend(["l(A)", "l(B)", "lower bound"], loc = "lower right")
axs[0].set_title("Smallest eigenvalue vs aspect ratio of X")

axs[1].plot(f_s, avgMaxEigA, '-r')
axs[1].plot(f_s, avgMaxEigB1, '-b')
axs[1].plot(f_s, np.mean(uBound, axis =0), '--b')
axs[1].legend(["l(A)", "l(B)", "upper bound"], loc = "lower right")
axs[1].set_title("Largest eigenvalue vs aspect ratio of X")

axs[2].semilogy(f_s, avgCondA, '-r')
axs[2].semilogy(f_s, avgCondB, '-b')
axs[2].semilogy(f_s, np.mean(uBound / lBound, axis =0), '--b')
axs[2].legend(["k(A)", "k(B)", "upper bound"], loc = "lower right")
axs[2].set_title("Condition number vs aspect ratio of X")
fig.show()




