#!/usr/bin/env python

import argparse
import numpy as np
from scipy import signal

def main():
    args = parse_arguments()
    print("lalala completar...")
    
#ARREGLAR AQUI, NO HACE FALTA PASAR EL ARREGLO DE TIEMPOS!!
def objective_fuction(x, args):
    model = args(0)
    Ts = args(1)
    real_frec = args(2)
    time = args(3)
    
    if model == 1:
        print()
    

def modelo_1(model_params, Ts):
    Ta = model_params[0]
    Tb = model_params[1]
    Tc = model_params[2]
    Td = model_params[3]
    K  = model_params[4]
    Kd = model_params[5]
    
    A = np.array([[0, 0, 0, -1/K], [Kd/Tb, 0, -1/Tb, 0], [Kd*Td/Tb,  1,  -Tc/Tb,  0], [0,  0,  1/Ta, -1/Ta]])
    B = np.array([[-1/K],[0],[0], [0]])
    C = np.array([[1,0,0,0]]);
    D = np.array([[0]]);  
    
    sys = signal.StateSpace(A,B,C,D)
    sys_k = sys.to_discrete(Ts)
    return sys_k

def parse_arguments():
    parser = argparse.ArgumentParser("Objective function value.")

    parser.add_argument(
        "-m",
        "--model",
        action = "store",
        required = True,
        help = "number of model to compare to data.",
    )
    parser.add_argument(
        "-d",
        "--data",
        action = "store",
        required = True,
        help = "path to *.csv file with data.",
    )

    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()