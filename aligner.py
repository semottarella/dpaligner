#!/usr/bin/python

import sys
from argparse import ArgumentParser

def printTable(t):
    for i in t:
        print i
    print

def main(argv):

    parser = ArgumentParser(description = "Needleman-Wunsch")
    parser.add_argument("string1", help="Input string")
    parser.add_argument("string2", help="Input string")
    parser.add_argument("--match", "-m", help="Match score", type=int, default=1)
    parser.add_argument("--mismatch", "-i", help="Mismatch score",
                        type=int, default=-1)
    parser.add_argument("--gap", "-g", help="Gap penalty", type=int, default=-4)
    parser.add_argument("--verbose", "-v", help="Verbose", action="store_true")
    parser.add_argument("--sw", help="Smith-Waterman", action="store_true")
    args = parser.parse_args()

    # align function
    def align(a, b):
        if a == b:
            return args.match
        return args.mismatch

    #Build a table
    #   string1-->
    # s [0, -4, -8, ...]
    # t [-4, 0, 0, ...]
    # r [-8, 0, 0, ...]
    # i [...]
    # n [...]
    # g [...]
    # 2 [...]
    # |
    # |
    # v
    table = [[0 for i in xrange(len(args.string1) + 1)] for j in 
                    xrange(len(args.string2) + 1)]

    # Fill table
    if not args.sw:
        for i in xrange(len(args.string1) + 1):
            table[0][i] = i * args.gap

        for j in xrange(len(args.string2) + 1):
            table[j][0] = j * args.gap

    if args.verbose:
        printTable(table)

    high = [0, 0, 0]
    for i in xrange(1, len(args.string1) + 1):
        for j in xrange(1, len(args.string2) + 1):
            if args.sw:
                table[j][i] = max(table[j-1][i-1] + align(args.string1[i-1],
                                                          args.string2[j-1]),
                                  table[j-1][i] + args.gap,
                                  table[j][i-1] + args.gap, 0)
                if table[j][i] > high[0]:
                    high = [table[j][i], i, j]
            else:
                table[j][i] = max(table[j-1][i-1] + align(args.string1[i-1],
                                                          args.string2[j-1]),
                                  table[j-1][i] + args.gap,
                                  table[j][i-1] + args.gap)

            if args.verbose:
                printTable(table)

    #Traceback
    alignment1 = ""
    alignment2 = ""
    i = len(args.string1)
    j = len(args.string2)
    if args.sw:
        i = high[1]
        j = high[2]

    while i > 0 or j > 0:
        if args.sw and table[j][i] == 0:
            break;

        elif i == 0:
            alignment1 = "-" + alignment1
            j = j - 1

        elif j == 0:
            alignment2 = "-" + alignment2
            i = i - 1

        elif table[j][i] == table[j-1][i-1] + align(args.string1[i-1],
                                                    args.string2[j-1]):
            alignment1 = args.string1[i-1] + alignment1
            alignment2 = args.string2[j-1] + alignment2
            i = i - 1
            j = j - 1

        elif table[j][i] == table[j-1][i] + args.gap:
            alignment1 = "-" + alignment1
            alignment2 = args.string2[j-1] + alignment2
            j = j - 1

        else:
            alignment1 = args.string1[i-1] + alignment1
            alignment2 = "-" + alignment2
            i = i - 1

        if args.verbose:
            print alignment1
            print alignment2
            print

    print alignment1
    print alignment2

if __name__ == "__main__":
    main(sys.argv)
