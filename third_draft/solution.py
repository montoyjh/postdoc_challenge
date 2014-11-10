from distributor import Distributor
import sys
import argparse

# Argument parsing
# sys.setrecursionlimit()
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f',metavar='FILES_FILENAME',
                    help='File containing file list',
                    required=True)
arg_parser.add_argument('-n',metavar='NODES_FILENAME',
                    help='File containing node list',
                    required=True)
arg_parser.add_argument('-o',metavar='OUTPUT_FILENAME',
                    help='output file, optional, default is stdout')
args = arg_parser.parse_args()

# Main body
dist = Distributor(args.f,args.n)
dist.distribute_iteratively()

dist.plot()
