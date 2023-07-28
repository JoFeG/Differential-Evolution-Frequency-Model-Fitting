#!/usr/bin/env python

import os 
import argparse
#import threading

def main():
    args = parse_arguments()
    if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
    
    if args.raw_plots:
        with os.scandir(args.input_dir) as entries:
            for entry in entries:
                if ".csv" in entry.name:
                    input_path = os.path.join(args.input_dir, entry.name)
                    pre, ext = os.path.splitext(entry.name)
                    output_path = os.path.join(args.output_dir, pre + "_raw.png")
                    source_path = os.path.join("src","plot_raw.py")
                    print("python " + source_path + " -i " + input_path + " -o " + output_path)
                    os.system("python " + source_path + " -i " + input_path + " -o " + output_path)

    if args.sampler:
        with os.scandir(args.input_dir) as entries:
            for entry in entries:
                if ".csv" in entry.name:
                    input_path = os.path.join(args.input_dir, entry.name)
                    source_path = os.path.join("src","sampler.py")
                    print("python " + source_path + " -i " + input_path + " -o " + args.output_dir)
                    os.system("python " + source_path + " -i " + input_path + " -o " + args.output_dir)
                                        
    if args.differential_evolution:
        with os.scandir(args.input_dir) as entries:
            for entry in entries:
                if ".csv" in entry.name:
                    input_path = os.path.join(args.input_dir, entry.name)
                    source_path = os.path.join("src","de_run.py")
                    print("python " + source_path + " -i " + input_path + " -o " + args.output_dir)
                    os.system("python " + source_path + " -i " + input_path + " -o " + args.output_dir + " -m cc") ## ARREGRAR ESTE HARCODED
    
def parse_arguments():
    parser = argparse.ArgumentParser(".")

        
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
    parser.add_argument(
        "-rp",
        "--raw-plots",
        action = "store_true",
        help = "generates all raw data plots from input directory",
    )
    parser.add_argument(
        "-sa",
        "--sampler",
        action = "store_true",
        help = "runs sampler script over all data from input directory",
    )
    parser.add_argument(
        "-de",
        "--differential-evolution",
        action = "store_true",
        help = "runs differential-evolution over all data from input directory",
    )
    return parser.parse_args()
    
    
if __name__ == "__main__":
    main()
