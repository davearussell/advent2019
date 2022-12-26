#! /usr/bin/python3
import sys


def get_points(wire):
    points = {} # (x, y) -> steps
    pos = (0, 0)
    steps = 0
    for dir_, dist in wire:
        if dir_ == 'R':
            new_points = [(pos[0] + i, pos[1]) for i in range(dist + 1)]
        elif dir_ == 'L':
            new_points = [(pos[0] - i, pos[1]) for i in range(dist + 1)]
        elif dir_ == 'U':
            new_points = [(pos[0], pos[1] - i) for i in range(dist + 1)]
        elif dir_ == 'D':
            new_points = [(pos[0], pos[1] + i) for i in range(dist + 1)]
        for i, point in enumerate(new_points):
            points.setdefault(point, steps + i)
        pos = new_points[-1]
        steps += dist
    return points



def main(input_file):
    wires = [
        [(x[0], int(x[1:])) for x in line.split(',')]
         for line in open(input_file).read().strip().split('\n')
    ]
    points = [get_points(wire) for wire in wires]
    intersections = set(points[0]) & set(points[1]) - {(0, 0)}
    
    dists = [abs(x) + abs(y) for x, y in intersections]
    print("Part 1:", min(dists))

    costs = [points[0][x] + points[1][x] for x in intersections]
    print("Part 2:", min(costs))


if __name__ == '__main__':
    main(sys.argv[1])
