#!/usr/bin/env python

import argparse
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def main():
    args = parse_arguments()
    plot_raw(args.input)
    plt.savefig(args.output)
    
def plot_raw(input_path, fig_size = (16, 7)):
    df = pd.read_csv(input_path)
    fig = plt.figure(figsize=fig_size)
    
    ## No todos los archivos tienen las mismas columnas CL_*
    ## La columna CIO es la media de las que si estan
    freq = [x for x in df.columns if "CL" in x]
    data = df[freq].to_numpy()
    time = 0.02 * np.arange(data.shape[0])
    
    
    ## Linea inicio evento
    plt.axvline(x = 0.02 * df["Inicio"][0], color = 'r')
    
    ## Plots CL_*
    plt.plot(time, data, alpha=.5)
    plt.legend(["Inicio Evento"]+freq)
    plt.title("Frecuencia " + input_path)
    plt.xlabel("tiempo relativo [seg]")
    plt.ylabel("frecuencia [Hz]")
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
        help = "path of plot, should end in *.png",
    )

    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
