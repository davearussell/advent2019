#! /usr/bin/python3
import sys

import numpy
import numba


@numba.njit(cache=True)
def make_patterns(n):
    base = [0, 1, 0, -1]
    patterns = numpy.zeros((n, n), dtype=numpy.int64)
    for i in range(n):
        for j in range(n):
            idx = ((j + 1) // (i + 1)) % 4
            patterns[i][j] = base[idx]
    return patterns


@numba.njit(cache=True)
def do_part1(data):
    patterns = make_patterns(len(data))
    for i in range(100):
        new_data = data.copy()
        for i in range(len(data)):
            x = sum(data * patterns[i])
            new_data[i] = x % 10 if x >= 0 else (-x) % 10
        data = new_data
    return data[:8]


@numba.njit(cache=True)
def do_part2(data):
    for i in range(100):
        for j in range(len(data) - 2, -1, -1):
            data[j] = (data[j] + data[j + 1]) % 10
    return data[:8]


def main(input_file):
    data = numpy.array([int(x) for x in open(input_file).read().strip()], dtype=numpy.int64)

    print("Part 1:", do_part1(data))

    p2_offset = int(''.join(str(x) for x in data[:7]))
    # For every entry in the second half of the sequence, its value after each transform
    # is equal to its pre-transform value plus the subsequent entry's post-transform value
    # (except the final value, which is always constant). This property makes calculating
    # values after each transform much quicker.
    assert p2_offset > len(data) / 2
    p2_data = numpy.tile(data, 10000)[p2_offset:]
    print("Part 2:", do_part2(p2_data))



if __name__ == '__main__':
    main(sys.argv[1])
