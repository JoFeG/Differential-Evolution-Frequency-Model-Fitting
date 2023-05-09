#!/usr/bin/env python

import argparse
import pandas as pd
from matplotlib import pyplot as plt

def main():
    args = parse_arguments()
    plot_result(args.input)
    plt.savefig(args.output)
    
def plot_result(input_path, fig_size = (16, 7)):
    df = pd.read_csv(input_path)
    fig = plt.figure(figsize=fig_size)
    

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
