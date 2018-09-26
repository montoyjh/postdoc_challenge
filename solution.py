# Author: J. Montoya - montoyjh@gmail.com

from distribution import Distribution
import argparse

# Argument parsing
desc = """
Program that takes two filename inputs corresponding to lists
of files and nodes and distributes the files onto the nodes
such that the absolute loads are evenly distributed
"""

arg_parser = argparse.ArgumentParser(description=desc)
arg_parser.add_argument('-f', '--files', help='File containing file list',
                        required=True)
arg_parser.add_argument('-n', '--nodes', help='File containing node list',
                        required=True)
arg_parser.add_argument('-o', '--output',
                        help='output file, optional, default is stdout')
arg_parser.add_argument('-p', '--plot', action='store_true',
                        help='plotting flag, plots nodes/files on bar chart')
arg_parser.add_argument('-pl', '--plotly', action='store_true',
                        help='plotting flag, plots nodes/files on bar chart'
                             'in plotly')
args = arg_parser.parse_args()

# Main body
if __name__ == "__main__":
    dist = Distribution.from_filenames(args.files, args.nodes)
    dist.summary(args.output)

    if args.plot:
        ply = dist.plot()
    if args.plotly:
        plt = dist.get_plotly()
