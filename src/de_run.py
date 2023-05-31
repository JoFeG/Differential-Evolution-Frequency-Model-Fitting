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
    result = differential_evolution(objective_function, bounds, args=(arguments,))
    
    
    ## SAVE REPORT
    head, tail = os.path.split(args.input_file)
    pre, ext = os.path.splitext(tail)
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
