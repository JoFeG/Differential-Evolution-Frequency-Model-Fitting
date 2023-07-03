import numpy as np
from scipy import signal

params = {
    "b"  : 5,
    "c"  : 6,
    "cc" : 5
}

def modelo_b(model_params, Ts):
    Ta, Tb, Tc, H, Kd = model_params

    A = np.array([
        [0,                    0,  -1/H], 
        [Kd*(Tb-Tc)/Tb**2, -1/Tb,     0], 
        [Kd*Tc/(Ta*Tb),     1/Ta, -1/Ta]
    ])
    B = np.array([
        [-1/H], 
        [0], 
        [0]
    ])
    
    C = np.array([[1, 0, 0]]);
    D = np.array([[0]]);  
    
    sys = signal.StateSpace(A,B,C,D)
    sys_k = sys.to_discrete(Ts)
    return sys_k

def modelo_c(model_params, Ts):
    Ta, Tb, Tc, Td, H, Kd = model_params

    A = np.array([
        [0,        0,      0,  -1/H], 
        [Kd/Tb,    0,  -1/Tb,     0], 
        [Kd*Td/Tb, 1, -Tc/Tb,     0], 
        [0,        0,   1/Ta, -1/Ta]
    ])
    B = np.array([
        [-1/H], 
        [0], 
        [0], 
        [0]
    ])
    
    C = np.array([[1, 0, 0, 0]]);
    D = np.array([[0]]);  
    
    sys = signal.StateSpace(A,B,C,D)
    sys_k = sys.to_discrete(Ts)
    return sys_k

def modelo_cc(model_params, Ts):
    Tb, Tc, Td, H, Kd = model_params

    A = np.array([
        [0,        0,   -1/H], 
        [Kd/Tb,    0,  -1/Tb], 
        [Kd*Td/Tb, 1, -Tc/Tb]
    ])
    B = np.array([
        [-1/H], 
        [0], 
        [0]
    ])
    C = np.array([[1, 0, 0]]);
    D = np.array([[0]]);  
    
    sys = signal.StateSpace(A,B,C,D)
    sys_k = sys.to_discrete(Ts)
    return sys_k