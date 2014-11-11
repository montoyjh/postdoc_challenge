# Author: J. Montoya - montoyjh@gmail.com

from distributor import Distributor
import sys
import argparse

# Argument parsing
desc = 'Program that takes two filename inputs corresponding \
        to lists of files and nodes and distributes the files \
        onto the nodes such that the absolute loads are as \
        close to one another as possible'
    
arg_parser = argparse.ArgumentParser(description=desc)
arg_parser.add_argument('-f',metavar='FILES_FILENAME',
                    help='File containing file list',
                    required=True)
arg_parser.add_argument('-n',metavar='NODES_FILENAME',
                    help='File containing node list',
                    required=True)
arg_parser.add_argument('-o',metavar='OUTPUT_FILENAME',
                    help='output file, optional, default is stdout')
arg_parser.add_argument('-p',action='store_true',
                    help='plotting flag, plots nodes/files on bar chart')
args = arg_parser.parse_args()

if args.o:
    sys.stdout = open(args.o,'w')
# Main body
dist = Distributor(args.f,args.n)
dist.distribute()
dist.summary()
if args.p:
    dist.plot()
