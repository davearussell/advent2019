#! /usr/bin/python3
import sys


def fuel(module):
    fuel = 0
    v = module // 3 - 2
    while v:
        fuel += v
        v = max(0, v // 3 - 2)
    return fuel


def main(input_file):
    values = [int(x) for x in open(input_file).read().split()]
    print("Part 1:", sum(x // 3 - 2 for x in values))
    print("Part 2:", sum(map(fuel, values)))


if __name__ == '__main__':
    main(sys.argv[1])
