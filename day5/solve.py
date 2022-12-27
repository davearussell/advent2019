#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def main(input_file):
    mem = intcode.load(input_file)
    print("Part 1:", intcode.run(mem.copy(), [1]))
    print("Part 2:", intcode.run(mem.copy(), [5]))


if __name__ == '__main__':
    main(sys.argv[1])
