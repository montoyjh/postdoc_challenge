import sys
import argparse
import random

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-o',metavar='OUTPUT_FILE',
                        help='Output file for file',
                        required=True)
arg_parser.add_argument('-n',metavar='NUM_DATA',
                        help='number of correctly formatted data entries',
                        default=10)
arg_parser.add_argument('-hashlines',metavar='NUM_HASH_LINES',
                        help='number of lines beginning with hashes',
                        default=0)
arg_parser.add_argument('-r',metavar='NUM_ERRORS',
                        help='number of random lines, i. e. potential errors',
                        default=0)
arg_parser.add_argument('-u',metavar='UPPER_LIMIT',
                        help='upper limit of value sizes',
                        default=10000)
arg_parser.add_argument('-l',metavar='LOWER_LIMIT',
                        help='lower limit of value sizes',
                        default=10)

args = arg_parser.parse_args()
f = open(args.o,'w')
outlines = []
for i in range(args.n):
    # Create random key 4-7 letters long
    key = ''.join([chr(random.randint(40,100)) \
                   for i in range(random.randint(4,8))])
    value=random.randint(args.l,args.u)
    outlines.append(' '.join([key,str(value)]))

for i in range(args.hashlines):
    outlines.append('#'+''.join([chr(random.randint(40,100)) \
                   for i in range(random.randint(4,8))]))

for i in range(args.r):
    outlines.append('#'+''.join([chr(random.randint(40,100)) \
                   for i in range(random.randint(4,8))]))

random.shuffle(outlines)
f.write('\n'.join(outlines))
