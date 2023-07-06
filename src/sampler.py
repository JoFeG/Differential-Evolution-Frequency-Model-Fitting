#!/usr/bin/env python

import os 
import argparse
import pandas as pd
import numpy as np
from scipy import signal

def main():
    args = parse_arguments()    
    df = sampler(
        args.input, 
        float(args.sampling_time), 
        float(args.event_time),
        float(args.nominal_frequency)
    )
    
    if os.path.isdir(args.output):
        head, tail = os.path.split(args.input)
        pre, ext = os.path.splitext(tail)
        output_path = os.path.join(args.output, pre + "_sampled.csv")
    else:
        output_path = args.output
    df.to_csv(output_path, index=False, float_format='%.6g')
    
    
def sampler(input_path, Ts, event_time=0, f0=50):
    df = pd.read_csv(input_path)
    # WARNING: This assumes 0.02 sampling time in the raw file!
    delta_i = int(Ts / 0.02) 
    
    delta_freq = df[df.index % delta_i == 0]["CIO"] - f0
    power =  df[df.index % delta_i == 0]["Potencia"]
    time = Ts * np.arange(delta_freq.size)
    event = (df[df.index % delta_i == 0].index >= df["Inicio"][0]).astype(int)
    nominal_frequency = np.repeat(f0, delta_freq.size)
    
    
    if event_time > 0:
        event[np.argmax(event) + int(np.ceil(event_time / Ts)):] = 0
    d = {'time':time, 'delta_freq':delta_freq, 'event':event, 'power':power, 'f0':nominal_frequency}
    df = pd.DataFrame(data=d)
    
    return df


def parse_arguments():
    parser = argparse.ArgumentParser("\nSample and aggregate data from a raw cvs file to a new cvs\nthat can be readed by objective_function.py, de_run.py, etc.\n")

    parser.add_argument(
        "-i",
        "--input",
        action = "store",
        required = True,
        help = "path to *.csv file with data (sampled each 0.02 seconds).",
    )
    parser.add_argument(
        "-o",
        "--output",
        action = "store",
        default = "out.csv",
        help = "path of output file, should end in *.csv or be a directory",
    )
    parser.add_argument(
        "-st",
        "--sampling-time",
        action = "store",
        default = .3,
        help = "sampling time in seconds (multiple of 0.02).",
    )
    parser.add_argument(
        "-et",
        "--event-time",
        action = "store",
        default = "30",
        help = "duration of the event in seconds",
    )
    parser.add_argument(
        "-nf",
        "--nominal-frequency",
        action = "store",
        default = "50",
        help = "nominal system electrical frequency f0",
    )
    
    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()