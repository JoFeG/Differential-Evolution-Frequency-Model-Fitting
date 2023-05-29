#!/usr/bin/env python

import argparse
import pandas as pd
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
    data = df[freq]
    
    ## Linea inicio evento
    plt.axvline(x = df["Inicio"][0], color = 'r')
    
    ## Plots CL_*
    plt.plot(data, alpha=.5)
    plt.legend(["Inicio Evento"]+freq)
    plt.title("Frecuencia " + input_path)
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
