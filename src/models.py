#!/usr/bin/env python

import argparse
import numpy as np
from scipy import signal

def modelo_1(Ta,Tb,Tc,Td,K,Kd,Ts):
    A = np.array([[0, 0, 0, -1/K], [Kd/Tb, 0, -1/Tb, 0], [Kd*Td/Tb,  1,  -Tc/Tb,  0], [0,  0,  1/Ta, -1/Ta]])
    B = np.array([[-1/K],[0],[0], [0]])
    C = np.array([[1,0,0,0]]);
    D = np.array([[0]]);  
    
    sys = signal.StateSpace(A,B,C,D)
    sys_k = sys.to_discrete(Ts)
    return sys_k