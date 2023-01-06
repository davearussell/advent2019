#! /usr/bin/python3
import math
import sys

import numba
import numpy


def parse_input(path):
    coords = []
    for line in open(path):
        coords.append([
            int(word.split('=', 1)[1])
            for word in line[1:-2].split(',')
        ])
    return numpy.array(coords)


@numba.njit
def step(moons, velocities):
    for a in range(len(moons)):
        for b in range(a + 1, len(moons)):
            delta = numpy.sign(moons[b] - moons[a])
            velocities[a] += delta
            velocities[b] -= delta

    for a in range(len(moons)):
        moons[a] += velocities[a]


def simulate_moons(moons, velocities, steps):
    for i in range(steps):
        step(moons, velocities)
    return energy(moons, velocities)


def find_period(moons, velocities, axis):
    period = 0
    seen = set()
    def make_key(ms, vs):
        return tuple(ms[:, axis].tolist() + vs[:, axis].tolist())
    while (key := make_key(moons, velocities)) not in seen:
        seen.add(key)
        period += 1
        step(moons, velocities)
    return period



def energy(moons, velocities):
    potential = numpy.apply_along_axis(lambda x: sum(abs(x)), 1, moons)
    kinetic = numpy.apply_along_axis(lambda x: sum(abs(x)), 1, velocities)
    return sum(potential * kinetic)


def main(input_file):
    moons = parse_input(input_file)
    velocities = numpy.zeros(moons.shape, dtype=numpy.int64)


    print("Part 1:", simulate_moons(moons.copy(), velocities.copy(), 1000))

    periods = [find_period(moons, velocities, axis) for axis in range(3)]
    print("Part 2:,", math.lcm(*periods))


if __name__ == '__main__':
    main(sys.argv[1])
