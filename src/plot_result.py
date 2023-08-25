#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal


import models as mdl

def main():
    args = parse_arguments()
    plot_result(args.input)
    plt.savefig(args.output)
    
def plot_result(df, args, x, fig_size = (16, 7)):
    
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
    
    real_time = df["time"].to_numpy()
    real_freq = df["delta_freq"].to_numpy()
    
    event_time = df["time"][df["event"]==1].to_numpy()
    #sim_time = np.arange(event_time[0],event_time[-1],Ts) # Esto genera un bug!
    sim_time = np.linspace(event_time[0],event_time[-1],num=sim_freq.size)

    fig = plt.figure(figsize=fig_size)
    
    plt.plot(real_time,real_freq)
    plt.axvspan(event_time.min(), event_time.max(), alpha=.1)
    
    plt.plot(sim_time,sim_freq)
    plt.xlabel("t [seg]")
    plt.ylabel("Δf [Hz]")
    
    return fig
    

def parse_arguments():
    parser = argparse.ArgumentParser("Plot raw data.")

    parser.add_argument(
        "-i",
        "--input",
        action = "store",
        required = True,
        help = "path to *.csv file with data.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action = "store",
        default = "./plot_raw.png",
        help = "path of plot, shoul end in *.png",
    )

    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
