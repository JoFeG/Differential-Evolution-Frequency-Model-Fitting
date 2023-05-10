#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np
from scipy import signal

def main():
    args = parse_arguments()
    sampler(args.input, float(args.time), args.output)
    
def sampler(input_path, Ts, output_path):
    df = pd.read_csv(input_path)
    delta_i = int(Ts / 0.02) # This asumes 0.02 sampling time in the raw file!
    
    freq = df[df.index % delta_i == 0]["CIO"]
    power =  df[df.index % delta_i == 0]["Potencia"]
    time = Ts * np.arange(freq.size)
    event = (df[df.index % delta_i == 0].index >= df["Inicio"][0]).astype(int)

    d = {'time':time, 'freq':freq, 'power':power, 'event':event}

    pd.DataFrame(data=d).to_csv(output_path, index=False, float_format='%.6g')
    
    return 1


def parse_arguments():
    parser = argparse.ArgumentParser("Sample and agregate data.")

    parser.add_argument(
        "-i",
        "--input",
        action = "store",
        required = True,
        help = "path to *.csv file with data (sampled each 0.02 seconds).",
    )
    parser.add_argument(
        "-t",
        "--time",
        action = "store",
        default = .3,
        help = "sampling time in seconds (multiple of 0.02).",
    )
    parser.add_argument(
        "-o",
        "--output",
        action = "store",
        default = "out.csv",
        help = "path of output file, should end in *.csv",
    )

    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()