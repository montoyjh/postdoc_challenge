"""Quick module for creating files for testing"""
import argparse
import uuid
from random import randint, shuffle


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-o',  '--output',
                        help='Output file for file',
                        required=True)
arg_parser.add_argument('-n', '--num_entries', type=int,
                        help='number of correctly formatted data entries',
                        default=10)
arg_parser.add_argument('-i', '--hash', type=int,
                        help='number of lines beginning with hashes',
                        default=0)
arg_parser.add_argument('-e', '--errors', type=int,
                        help='number of random lines, i. e. potential errors',
                        default=0)
arg_parser.add_argument('-u', '--upper', type=int,
                        help='upper limit of value sizes',
                        default=10000)
arg_parser.add_argument('-l', '--lower', type=int,
                        help='lower limit of value sizes',
                        default=10)
arg_parser.add_argument('-p', '--prefix', default="node",
                        help="prefix for node/file titles, defaults to 'node'")



args = arg_parser.parse_args()

if __name__ == "__main__":
    outlines = []
    outlines += ["{}_{} {}".format(args.prefix, n,
                                   randint(args.lower, args.upper))
                 for n in range(args.num_entries)]
    outlines += ["#{}".format(uuid.uuid4())]
    outlines += [uuid.uuid4() for n in range(args.errors)]

    shuffle(outlines)

    with open(args.output, 'w') as f:
        f.write('\n'.join(outlines))
