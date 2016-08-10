# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:34:51 2016

@author: raon
"""

import numpy as np
import scipy.sparse as sp


def vec(X):
    return np.ravel(X.T)

def HV(L,A,S,O):
    """
    Hessian-Vect multiplication according to GRALS, Alg 2
    L = laplacian, A = (W,H) fixed, S = (W,H) to be updated, O = corresponding Omega
    """
    k,n = np.shape(S)
    K   = np.zeros((k,n))                               # kxn
    for j in xrange(n):
        ind_to_sum = O[j]                               # lx1
        A_temp = A[ind_to_sum,:]                        # lxk 
        K[:,j] = np.dot(A_temp.T,np.dot(A_temp,S[:,j])) # kx1
    
    F = K + sp.csr_matrix.dot(S,L)                      # kxn
    return vec(F)


def conjgrad(Y,L,A,S,O):
    
    b = vec(sp.coo_matrix.dot(A.T,Y))
    r = b
    p = r
    rsold = np.inner(r,r)
    x = np.zeros(p.shape())
    
    for i in range(b.shape[0]):
        p = vec(S.T)
        Ap = HV(L,A,S,O)
        alpha = rsold/(np.inner(p,Ap))
        x += alpha*p
        r -= alpha*Ap
        rsnew = np.inner(r,r)
        if np.sqrt(rsnew)<1e-10:
            break
        p = r + (rsnew/rsold)*p
        rsold=rsnew
        S = np.reshape(p,S.shape())
    
    return np.reshape(x,S.shape())
    

