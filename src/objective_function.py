#!/usr/bin/env python

import argparse
import numpy as np
from scipy import signal

def main():
    args = parse_arguments()
    print("lalala completar...")
    
def objective_function(x, args):
    model, Ts, P0, x0, real_freq = args
    # Ojo con las unidades! 
    # El Ts del modelo y de real_frec tienen que ser el mismo!
    
    if model == 1:
        sys = modelo_1(x, Ts)
        
    sim_power = P0 * np.repeat(1, real_freq.shape)
    sim = signal.dlsim(sys, sim_power, x0 = real_freq[0])
    sim_freq = sim[1].ravel()
        
    ssd = np.sum((sim_freq - real_freq)**2)
    return ssd

def modelo_1(model_params, Ts):
    Ta, Tb, Tc, Td, K, Kd = model_params

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