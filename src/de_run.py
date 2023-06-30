#!/usr/bin/env python

import os 
import argparse
import pickle
import pandas as pd
import numpy as np

from scipy import signal
from scipy.optimize import differential_evolution
from matplotlib import pyplot as plt

from models import modelo_c
from plot_result import plot_result

def objective_function(x, args):
    model, Ts, P0, real_freq = args
    
    if model == "c":
        sys = modelo_c(x, Ts)
        
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
    event_time = Ts*(np.sum(df["event"][df["event"]==1].to_numpy())-1)
    
        
    P0 = df["power"][0] / 1000
    
    event_freq = df["freq"][df["event"]==1].to_numpy()
    
    #################################################################### OJO
    event_freq = event_freq - 50
    #################################################################### OJO
    
    bounds = [(0.00001, 1000) for i in range(6)] ## CHECK
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
        recombination = recombination
    )
    
    ## FOR OUTPUTS
    head, tail = os.path.split(args.input_file)
    pre, ext = os.path.splitext(tail)
    
    if args.output_dir != "":
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
        fig = plot_result(df, arguments, result.x)
        plt.text(0, min(event_freq), repr(result), fontsize=10, fontfamily='monospace')
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
        "-p",
        "--parameters",
        action = "store",
        default = "",
        help = "differential optization parameters separated by comas:\npopsize,mutation,recombination,[maxiter,tol]",
    )

    
    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
