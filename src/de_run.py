#!/usr/bin/env python

import os 
import argparse
import pickle
#import threading

from scipy.optimize import differential_evolution
from matplotlib import pyplot as plt

from sampler import sampler
from objective_function import objective_function
from plot_result import plot_result

def main():
    args = parse_arguments()
    
    model = int(args.model)
    Ts = float(args.sampling_time)
    event_time = float(args.event_time)
    df = sampler(args.input_file, Ts, event_time=event_time)
    
    
    P0 = df["power"][0] / 1000
    
    event_freq = df["freq"][df["event"]==1].to_numpy()
    bounds = [(0.00001, 1000) for i in range(6)] ## CHECK
    arguments = (model, Ts, P0, event_freq)
    
    popsize = 30
    tol = 0.01
    mutation = (0.5, 1.5)
    recombination = 0.6
    
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
    
    print(tail)
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
        default = "./out",
        help = "path to path output directory",
    )
    parser.add_argument(
        "-m",
        "--model",
        action = "store",
        default = "1",
        help = "model number for simulation",
    )
    parser.add_argument(
        "-st",
        "--sampling-time",
        action = "store",
        default = ".3",
        help = "time interval (in seconds) to sample from row and to run simulations",
    )
    parser.add_argument(
        "-et",
        "--event-time",
        action = "store",
        default = "25",
        help = "duration of the event in seconds",
    )
    
    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
