#!/usr/bin/env python

import os 
import argparse

def main():
    args = parse_arguments()
    
    with os.scandir(args.input_dir) as entries:
        for entry in entries:
            if ".csv" in entry.name:
                input_path = args.input_dir + entry.name
                output_path = args.output_dir + "/" + entry.name[0:-3] + "png"
                os.system("./src/plot_raw.py -i " + input_path + " -o " + output_path)
    
def parse_arguments():
    parser = argparse.ArgumentParser("Generate all raw data plots from directory.")

    parser.add_argument(
        "-i",
        "--input-dir",
        action = "store",
        required = True,
        help = "path to directory containing data in *.csv form.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        action = "store",
        default = "./out",
        help = "path to path output directory",
    )

    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
