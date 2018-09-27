"""Quick module for creating files for testing"""
import argparse
import uuid
from random import randint, shuffle


def generate_text(num_entries, prefix='files', errors=0,
                       upper=10000, lower=10, hashlines=0):
    """Generates some test text for parsing"""
    outlines = []
    outlines += ["{}_{} {}".format(prefix, n,
                                   randint(lower, upper))
                 for n in range(num_entries)]
    outlines += ["#{}".format(uuid.uuid4()) for _ in range(hashlines)]
    outlines += [uuid.uuid4() for _ in range(errors)]

    shuffle(outlines)
    return '\n'.join(outlines)


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


if __name__ == "__main__":
    args = arg_parser.parse_args()
    text = generate_text(args.num_entries, args.prefix, args.errors,
                              args.upper, args.lower, args.hash)
    with open(args.output, 'w') as f:
        f.write(text)
