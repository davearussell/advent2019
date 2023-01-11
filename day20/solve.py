#! /usr/bin/python3
import sys


def parse_input(path):
    data = open(path).read().rstrip('\n')

    rows = data.split('\n')
    pathable = set()
    portals = {}
    start = goal = None

    width = len(rows[0]) - 4
    height = len(rows) - 4

    for donut_width, row in enumerate(rows[2:]):
        if set(row[2:-2]) - {'#', '.'}:
            break

    for y, row in enumerate(rows[2:-2]):
        for x, cell in enumerate(row[2:-2]):
            if cell == '.':
                pathable.add((x, y))

    portal_pairs = {}
    for x in range(width):
        for y, offset in [(0, -1),
                          (donut_width - 1, 1),
                          (height - donut_width, -1),
                          (height - 1, 1)]:
            a = rows[y + 2 + offset][x + 2]
            b = rows[y + 2 + offset * 2][x + 2]
            if a.isupper() and b.isupper():
                name =  a + b if offset > 0 else b + a
                if name == 'AA':
                    start = (x, y, 0)
                elif name == 'ZZ':
                    goal = (x, y, 0)
                else:
                    is_outer = y in [0, height - 1]
                    portal_pairs.setdefault(name, []).append((x, y, is_outer))

    for y in range(height):
        for x, offset in [(0, -1),
                         (donut_width - 1, 1),
                         (width - donut_width, -1),
                         (width - 1, 1)]:
            a = rows[y + 2][x + 2 + offset]
            b = rows[y + 2][x + 2 + offset * 2]
            if a.isupper() and b.isupper():
                name =  a + b if offset > 0 else b + a
                if name == 'AA':
                    start = (x, y, 0)
                elif name == 'ZZ':
                    goal = (x, y, 0)
                else:
                    is_outer = x in [0, width - 1]
                    portal_pairs.setdefault(name, []).append((x, y, is_outer))

    assert all(len(p) == 2 for p in portal_pairs.values())
    portals = {}
    for (ax, ay, a_is_outer), (bx, by, b_is_outer) in portal_pairs.values():
        assert a_is_outer != b_is_outer
        portals[(ax, ay)] = (bx, by, 1 if b_is_outer else -1)
        portals[(bx, by)] = (ax, ay, 1 if a_is_outer else -1)

    return pathable, portals, start, goal


def plot_path(pathable, portals, start, goal, recurse):
    visited = set()
    frontier = {start}
    distance = 0
    while frontier:
        if goal in frontier:
            return distance
        new_frontier = set()
        for x, y, z in frontier:
            neighbours = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & pathable
            new_frontier |= {(x, y, z) for (x, y) in neighbours}
            if (x, y) in portals:
                px, py, pz = portals[(x, y)]
                if recurse:
                    if 0 <= z + pz <= len(portals):
                        new_frontier.add((px, py, z + pz))
                else:
                    new_frontier.add((px, py, z))
        visited |= frontier
        frontier = new_frontier - visited
        distance += 1


def main(input_file):
    pathable, portals, start, goal = parse_input(input_file)
    print("Part 1:", plot_path(pathable, portals, start, goal, False))
    print("Part 2:", plot_path(pathable, portals, start, goal, True))


if __name__ == '__main__':
    main(sys.argv[1])
