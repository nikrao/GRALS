# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 20:38:42 2016

@author: raon
"""

import numpy as np
import scipy.sparse as sp
import graph_preprocess as gp
import data_preprocess as dp
import evaluations as evals



def main(trainfile,testfile=None,Ugraph=None,Vgraph=None,split=0.2,lam=0.1,mu=0.01,max_iter=20):
    """
    GRALS
    """
    # data preprocessing
    TRAIN,TEST,Oi_train,Oj_train,Oi_test,Oj_test = dp.make_train_test_split(trainfile,testfile,split)

    m,n = TRAIN.shape()    
    
    # graph laplacian
    if Ugraph==None:
        L1 = sp.eye(m)
    else:
        G = gp.make_graph(Ugraph)
        L1 = gp.get_laplacian(G)
        
    if Vgraph==None:
        L2 = sp.eye(n)
    else:
        G = gp.make_graph(Vgraph)
        L2 = gp.get_laplacian(G)
    
    

if __name__=='__main__':
    import sys
    for i in range(1,len(sys.argv),2):
        if sys.argv[i]=='-train':
            train = sys.argv[i+1]
        elif sys.argv[i]=='-test':
            test = sys.argv[i+1]
        elif sys.argv[i]=='-split':
            split = sys.argv[i+1]
        elif sys.argv[i]=='-lam':
            lam = sys.argv[i+1]
        elif sys.argv[i]=='-mu':
            mu = sys.argv[i+1]
        elif sys.argv[i]=='-iter':
            max_iter = sys.argv[i+1]
        elif sys.argv[i]=='-ug':
            Ugraph = sys.argv[i+1]
        elif sys.argv[i]=='-vg':
            Vgraph = sys.argv[i+1]