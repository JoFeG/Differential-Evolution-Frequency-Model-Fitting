#!/usr/bin/env python

import os 
import argparse
#import threading

from scipy.optimize import differential_evolution

from sampler import sampler
from objective_function import objective_function

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
    print(result.x)
    
    ## SAVE REPORT
    
    ## SAVE RESULT PLOT
    
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
