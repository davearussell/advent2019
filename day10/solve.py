#! /usr/bin/python3
import math
import sys


def parse_input(path):
    asteroids = set()
    for y, row in enumerate(open(path)):
        for x, cell in enumerate(row):
            if cell == '#':
                asteroids.add((x, y))
    return asteroids


def length(path):
    return abs(path[0]) + abs(path[1])


def find_visible(asteroid, asteroids):
    x, y = asteroid
    paths = [(ox - x, oy - y) for ox, oy in asteroids]
    paths.sort(key=length)
    max_dist = length(paths[-1])
    hidden = set()
    visible = set()
    for path in paths[1:]: # paths[0] is to the asteroid itself
        x, y = path
        if path in hidden:
            continue
        g = math.gcd(x, y)
        vx, vy = (x // g, y // g)
        i = 1
        while True:
            hide = (x + vx * i, y + vy * i)
            if length(hide) > max_dist:
                break
            hidden.add(hide)
            i += 1
        visible.add(path)
    return visible


def vaporize_prio(path):
    x, y = path
    if x == 0:
        return (0 if y < 0 else 2, 0)
    elif x > 0:
        return (1, y / x)
    else:
        return (3, y / x)


def vaporize(asteroid, asteroids):
    x, y = asteroid
    paths = {(ox - x, oy - y) for ox, oy in asteroids}
    order = []
    while len(paths) > 1:
        visible = find_visible((0, 0), paths)
        order += sorted(visible, key=vaporize_prio)
        paths -= visible
    return [(ox + x, oy + y) for (ox, oy) in order]


def main(input_file):
    asteroids = parse_input(input_file)
    count, asteroid = max((len(find_visible(a, asteroids)), a) for a in asteroids)
    print("Part 1:", count)
    paths = vaporize(asteroid, asteroids)
    print("Part 2:", paths[199][0] * 100 + paths[199][1])


if __name__ == '__main__':
    main(sys.argv[1])
