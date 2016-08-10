# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 10:48:02 2016

@author: raon
"""

import scipy.sparse as sp
import numpy as np

def make_graph(gfile):
    """
    gfile is path to csv or txt file
    """
    row = []
    col = []
    data = []
    
    with open(gfile) as f:
        for line in f:
            temp = map(int,line.split()[0:2])
            data.append(float(line.split()[-1]))
            row.append(temp[0])
            col.append(temp[1])

    G = sp.coo_matrix((data,(row,col)))
    return G

def get_laplacian(G,Ltype=0):
    """
    G is a sparse matrix in coo format
    """
    G = sp.csr_matrix(G)
    n = G.shape[0]
    s = np.ravel(G.sum(axis=1))
    D = sp.diags(s,0,shape=(n,n))
    L = D-G
    if Ltype==1: # symmetric laplacian
        s = s**(-0.5)
        D = sp.diags(s,0,shape=(n,n))
        L = D.dot(L.dot(D))
    elif Ltype>1:
        s = s**(-1)
        D = sp.diags(s,0,shape=(n,n))
        L = D.dot(L)
        
    return L
    
if __name__=='__main__':
    import sys
    gfile = sys.argv[1]
    G = make_graph(gfile)
    L = get_laplacian(G)
    print L.shape
    print L.todense()
            
        