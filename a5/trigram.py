import sys
import os
import argparse
from glob import glob
import random
from trimodule import TrigramModelWithDistribution, TrigramModelWithTopK

# Write a script that takes a directory of text files and counts all
# the character trigrams. Then predicts a certain number of characters
# from the model.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and evaluate trigram model for characters.")
    parser.add_argument("--topk", action="store_true", help="Use topk instead.")
    parser.add_argument("directory", type=str, help="Name of the directory to be modeled.")
    parser.add_argument("number", type=int, help="Number of characters to generate.")
    parser.add_argument("seed", type=str, help="First two characters.")
    parser.add_argument("k", type=int, nargs='?', help="Number of topK.")

    args = parser.parse_args()

    allfiles = glob("{}/*.txt".format(args.directory))
    #print(allfiles)

    # accumulate everything in the files
    totalstring = ""
    for filename in allfiles:
        with open(filename, "r") as thefile:
            for line in thefile:
                totalstring += "\n" + line

    if not args.topk:
        model = TrigramModelWithDistribution(totalstring, args.number, args.seed)
    else:
        model = TrigramModelWithTopK(totalstring, args.number, args.seed, args.k)

    outputstring = "Final output: "
    for character in model:
        outputstring += character

    print(outputstring)
