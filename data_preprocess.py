# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 18:13:22 2016

@author: raon
"""

import scipy.sparse as sp
import numpy as np

def get_omega_dict(row,col):
    Oi,Oj = {},{}
    for ind in xrange(len(row)):
        i = row[ind]
        j = col[ind]
        if i not in Oi.keys():
            Oi[i] = [j]
        else:
            Oi[i].append(j)
            
        if j not in Oj.keys():
            Oj[j] = [i]
        else:
            Oj[j].append(i)
    
    return Oi,Oj

def make_train_test_split(trainfile,testfile=None,split=0.2):
    row,col,data = [],[],[]
    with open(trainfile) as T:
        for line in T:
            temp = map(int,line.split()[0:2])
            data.append(float(line.split()[-1]))
            row.append(temp[0])
            col.append(temp[1])
            
    if testfile is not None:
        TRAIN = sp.coo_matrix((data,(row,col)))
        Oi_train,Oj_train = get_omega_dict(row,col)
        with open(testfile) as T:
            for line in T:
                temp = map(int,line.split()[0:2])
                data.append(float(line.split()[-1]))
                row.append(temp[0])
                col.append(temp[1])
                
        TEST = sp.coo_matrix((data,(row,col)))
        Oi_test,Oj_test = get_omega_dict(row,col)
    else:
        N = len(row)
        from numpy.random import choice
        t_ind = choice(N,int(np.floor(split*N)))
        t_data = [data[i] for i in t_ind]
        t_row  = [row[i] for i in t_ind]
        t_col  = [col[i] for i in t_ind]
        TEST = sp.coo_matrix((t_data,(t_row,t_col)))
        Oi_test,Oj_test = get_omega_dict(t_row,t_col)
        
        t_ind = list(set(range(N)) - set(t_ind))
        t_data = [data[i] for i in t_ind]
        t_row  = [row[i] for i in t_ind]
        t_col  = [col[i] for i in t_ind]
        TRAIN = sp.coo_matrix((t_data,(t_row,t_col)))
        Oi_train,Oj_train = get_omega_dict(t_row,t_col)
   
    return TRAIN,TEST,Oi_train,Oj_train,Oi_test,Oj_test
    
def make_PU(DATA,thr=3.5):
    data = DATA.data
    row = DATA.row
    col = DATA.col
    data[data>thr]=1
    data[data<=thr]=0
    DATA = sp.coo_matrix((data,(row,col)))
    return DATA
    
if __name__=='__main__':
    import sys
    trainfile = sys.argv[1]
    Rtr,Rtt,Oi_t,Oj_t,Oi_test,Oj_test = make_train_test_split(trainfile)
    print 'test data'
    print Rtt
    print 'I dictionary'
    print Oi_test
    print 'J dictionary'
    print Oj_test