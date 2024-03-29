#!/usr/bin/env python

import os 
import argparse
import pickle
import pandas as pd
import numpy as np

from scipy import signal
from scipy.optimize import differential_evolution
from matplotlib import pyplot as plt

import models as mdl
from plot_result import plot_result

def objective_function(x, args):
    model, Ts, P0, real_freq = args
    
    if model == "b":
        sys = mdl.modelo_b(x, Ts)
    elif model == "c":
        sys = mdl.modelo_c(x, Ts)
    elif model == "cc":
        sys = mdl.modelo_cc(x, Ts)
    ########################################
    elif model == "A1":
        sys = mdl.modelo_A1(x, Ts)
    elif model == "A2":
        sys = mdl.modelo_A2(x, Ts)
    elif model == "B1":
        sys = mdl.modelo_B1(x, Ts)
    elif model == "B2":
        sys = mdl.modelo_B2(x, Ts)
        
    sim_power = P0 * np.repeat(1, real_freq.shape)
    sim = signal.dlsim(sys, sim_power, x0 = real_freq[0])
    sim_freq = sim[1].ravel()
        
    ssd = np.sum((sim_freq - real_freq)**2)
    #print(ssd)
    return ssd

def main():
    args = parse_arguments()
    
    model = args.model
    df = pd.read_csv(args.input_file)    
    Ts = df["time"][1]
    
    
    dt0 = int(args.delta_t0)
    
    # event_time = Ts*(np.sum(df["event"][df["event"]==1].to_numpy())-1)
    event_time = Ts*(np.sum(df["event"][df["event"]==1].to_numpy())-1-dt0)
    
        
    P0 = -df["power"][0] / 1000 # esto en realidad es ΔP_k en la notacion del modelo: que unidades tiene??
    f0 = df["f0"][0]
    
    # event_freq = df["delta_freq"][df["event"]==1].to_numpy()
    df['event_s'] = df['event'].shift(dt0)
    if dt0 < 0:
        event_freq = df["delta_freq"][(df["event"]==1)|(df["event_s"]==1)].to_numpy()
    else:
        event_freq = df["delta_freq"][(df["event"]==1)&(df["event_s"]==1)].to_numpy()
    
    
    bounds = [(0.001, 1000) for i in range(mdl.params[model])] ## CHECK THIS SOLUTION
    
    if args.hat_K != "":
        hat_K_strs = args.hat_K.split(",")
        hat_K = float(hat_K_strs[0])
        if len(hat_K_strs) > 1:
            EPS = float(hat_K_strs[1])
        else:
            EPS = .99 * hat_K    
    else:
        ###### K empirical estimation ######
        # first step derivative aprox:
        hat_K = (f0 * P0 / 2) / ((event_freq[1] - event_freq[0]) / Ts) 
        EPS = .99 * hat_K  
        
    K_min = hat_K - EPS
    K_max = hat_K + EPS    
    bounds[-2] = ((2/f0)*K_min, (2/f0)*K_max)
    
    if args.hat_Kd != "":
        hat_Kd_strs = args.hat_Kd.split(",")
        hat_Kd = float(hat_Kd_strs[0])
        if len(hat_Kd_strs) > 1:
            EPS = float(hat_Kd_strs[1])
        else:
            EPS = .7 * hat_Kd
    else:
        ###### Kd empirical estimation #####
        # last M freqs mean:
        M = 8
        event_ss_freq = sum(event_freq[-M:] / M)
        hat_Kd = P0 / event_ss_freq
        EPS = .7 * hat_Kd
    
    Kd_min = hat_Kd - EPS
    Kd_max = hat_Kd + EPS    
    bounds[-1] = (Kd_min, Kd_max)
    
    print(f"\nbounds_H = {[round(i,4) for i in bounds[-2]]}")
    print(f"bounds_Kd = {[round(i,4) for i in bounds[-1]] }\n")
    
    arguments = (model, Ts, P0, event_freq)
    
    if args.parameters != "":
        param_strs = args.parameters.split(",") 
        popsize = int(param_strs[0])
        mutation = float(param_strs[1])
        recombination = float(param_strs[2])
        if len(param_strs) == 5:
            maxiter = int(param_strs[3])
            tol = float(param_strs[4])
        else:
            maxiter = 1000
            tol = 0.01    
    else:
        # Default values
        popsize = 15
        mutation = 0.75  # can be interval (min, max), will change at each iteration. 
        recombination = 0.7
        maxiter = 1000
        tol = 0.01
            
    
    ## Collect information for convergence plot 
    obj_fun_vavues = []
    best_x_iterk = []
    conv_prop_iterk = []
    def callback(xk, convergence):
        ## WARNING: is this ok on parallelization? convergence plots could be wrong... (to check)
        try: 
            obj_fun_vavues.append(objective_function(xk, arguments))
            best_x_iterk.append(xk)
            conv_prop_iterk.append(convergence)
        except NameError:
            print("missing some of the arrays: obj_fun_vavues, best_x_iterk, conv_prop_iterk")

    ## Differential Evolution Run
    result = differential_evolution(
        objective_function, 
        bounds, 
        args=(arguments,),
        callback = callback,
        tol = tol,
        popsize = popsize,      
        mutation = mutation, 
        recombination = recombination,
        polish=False
    )
    
    ## FOR OUTPUTS
    head, tail = os.path.split(args.input_file)
    pre, ext = os.path.splitext(tail)
    
    if args.output_dir != "":
        if not os.path.isdir(args.output_dir):
            os.makedirs(args.output_dir)
        ## CONVERGENCE PLOT
        fig, ax1 = plt.subplots(figsize=(16, 7))
        ax1.plot(obj_fun_vavues, label = "Objective function value")
        ax2 = ax1.twinx()
        ax2.plot(conv_prop_iterk, color = 'red', alpha = .5, label = "Proportion of population convergence ")
        ax1.legend(loc =  'upper left')
        ax2.legend(loc = 'upper right')
        plt.title(tail)
        ax2.text(50, .5, f"model = {model}\nTs = {Ts}\nevent_time = {event_time}\n\ntol = {tol}\npopsize = {popsize}\nmutation = {mutation}\nrecombination = {recombination}", fontsize=10, fontfamily='monospace' )

        output_path = os.path.join(args.output_dir, pre + "_convergence.png")
        plt.savefig(output_path)


        ## SAVE REPORT    
        output_path = os.path.join(args.output_dir, pre + "_result.p")
        pickle.dump(result, open(output_path, "wb" ) )

        ## SAVE RESULT PLOT
        fig = plot_result(df, arguments, result.x, dt0=dt0)
        plt.text(0, min(event_freq), repr(result), fontsize=10, fontfamily='monospace')
        plt.text(event_time, (max(event_freq)+min(event_freq))/2, f"model = {model}\nTs = {Ts}\nevent_time = {event_time}\n\ntol = {tol}\npopsize = {popsize}\nmutation = {mutation}\nrecombination = {recombination}", fontsize=10, fontfamily='monospace' )
        plt.title(tail)

        output_path = os.path.join(args.output_dir, pre + "_result.png")
        plt.savefig(output_path)
    
    print("------------------------------------------------------------------------------------")
    print("   input:",tail,"\n")
    print(f"          model: {model}\n             Ts: {Ts}\n\n        popsize: {popsize}\n       mutation: {mutation}\n  recombination: {recombination}\n        maxiter: {maxiter}\n            tol: {tol}\n\n")
    print(result)
    print("------------------------------------------------------------------------------------")



def parse_arguments():
    parser = argparse.ArgumentParser(".")

    parser.add_argument(
        "-i",
        "--input-file",
        action = "store",
        required = True,
        help = "path to *.csv file.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        action = "store",
        default = "",
        help = "path to path output directory",
    )
    parser.add_argument(
        "-m",
        "--model",
        action = "store",
        default = "c",
        help = "model number for simulation",
    )
    parser.add_argument(
        "-K",
        "--hat-K",
        action = "store",
        default = "",
        help = "K estimated value",
    )
    parser.add_argument(
        "-Kd",
        "--hat-Kd",
        action = "store",
        default = "",
        help = "Kd estimated value",
    )
    parser.add_argument(
        "-dt0",
        "--delta-t0",
        action = "store",
        default = "0",
        help = "number of steps of sift in the event time start (positive or negative)",
    )
    parser.add_argument(
        "-p",
        "--parameters",
        action = "store",
        default = "",
        help = "differential optization parameters separated by comas:\npopsize,mutation,recombination,[maxiter,tol]",
    )

    
    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
