#! /usr/bin/python3
import sys


def parse_input(path):
    rows = open(path).read().split('\n')
    bugs = set()
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell == '#':
                bugs.add((x, y, 0))
    return bugs


def simple_neighbours(bug):
    x, y, z = bug
    return {(X, Y, z) for (X, Y) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            if 0 <= X < 5 and 0 <= Y < 5}


def recursive_neighbours(bug):
    x, y, z = bug
    neighbours = simple_neighbours(bug) - {(2, 2, z)}
    if y == 0:
        neighbours.add((2, 1, z - 1))
    if y == 4:
        neighbours.add((2, 3, z - 1))
    if x == 0:
        neighbours.add((1, 2, z - 1))
    if x == 4:
        neighbours.add((3, 2, z - 1))
    if (x, y) == (2, 1):
        neighbours |= {(X, 0, z + 1) for X in range(5)}
    if (x, y) == (2, 3):
        neighbours |= {(X, 4, z + 1) for X in range(5)}
    if (x, y) == (1, 2):
        neighbours |= {(0, Y, z + 1) for Y in range(5)}
    if (x, y) == (3, 2):
        neighbours |= {(4, Y, z + 1) for Y in range(5)}
    return neighbours


def iterate(bugs, neighbours):
    todo = bugs | {n for bug in bugs for n in neighbours(bug)}
    new_bugs = set()
    for pos in todo:
            alive = pos in bugs
            n = len(neighbours(pos) & bugs)
            if n == 1 or (not alive and n == 2):
                new_bugs.add(pos)
    return new_bugs


def score(bugs):
    return sum((1 << (y * 5 + x)) for (x, y, _) in bugs)


def main(input_file):
    initial_bugs = parse_input(input_file)

    seen = set()
    bugs = initial_bugs
    while True:
        bugs = iterate(bugs, simple_neighbours)
        k = tuple(bugs)
        if k in seen:
            print("Part 1:", score(bugs))
            break
        seen.add(k)

    bugs = initial_bugs
    for i in range(200):
        bugs = iterate(bugs, recursive_neighbours)
    print("Part 2:", len(bugs))
    




if __name__ == '__main__':
    main(sys.argv[1])
