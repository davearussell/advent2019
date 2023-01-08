#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode

WALL, FREE, OXY = range(3)


def neighbours(pos):
    x, y = pos
    return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}


def make_edges(grid):
    edges = {}
    for pos, v in grid.items():
        if v == WALL:
            continue
        edges[pos] = {n for n in neighbours(pos) if grid.get(n) != WALL}
    return edges


def find_paths(grid, start):
    edges = make_edges(grid)
    steps = {}
    frontier = {start}

    while frontier:
        new_frontier = set()
        for pos in frontier:
            neighbours = edges.get(pos, set()) - (set(steps) | {start})
            steps |= {neighbour: pos for neighbour in neighbours}
            new_frontier |= neighbours
        frontier = new_frontier

    paths = {start: []}
    while steps:
        for pos_to, pos_from in list(steps.items()):
            if pos_from in paths:
                paths[pos_to] = paths[pos_from] + [pos_to]
                del steps[pos_to]

    return paths


def follow_path(robot, start, path):
    cmds = {(0, -1): 1, (0, 1): 2, (-1, 0): 3, (1, 0): 4}
    for i, pos in enumerate(path):
        offset = (pos[0] - start[0], pos[1] - start[1])
        start = pos
        robot.run(cmds[offset])
        output = robot.outputs.pop(0)
        if i == len(path) - 1:
            return output
        assert output in [1, 2], output


def explore(robot):
    pos = (0, 0)
    grid = {pos: FREE}
    oxygen = None

    to_explore = neighbours(pos)
    while to_explore:
        paths = find_paths(grid, pos)
        target = min(to_explore, key=lambda pos: len(paths[pos]))
        to_explore.remove(target)
        path = paths[target]
        result = follow_path(robot, pos, path)
        grid[target] = result
        if result == WALL:
            if len(path) > 1:
                pos = path[-2]
        else:
            if result == OXY:
                oxygen = target
            to_explore |= (neighbours(target) - set(grid))
            pos = target
        print('\x1b[;H\x1b[J' + render_grid(grid))
    return grid, oxygen


def render_grid(grid):
    maxx = max(x for (x, y) in grid)
    minx = min(x for (x, y) in grid)
    maxy = max(y for (x, y) in grid)
    miny = min(y for (x, y) in grid)
    rendered = ''
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if x == y == 0:
                rendered += 'X'
            else:
                v = grid.get((x, y))
                rendered += {None: ' ', FREE: '.', WALL: '█', OXY: 'O'}[v]
        rendered += '\n'
    return rendered


def main(input_file):
    mem = intcode.load(input_file)
    robot = intcode.Process(mem)
    grid, oxygen = explore(robot)
    paths = find_paths(grid, oxygen)
    print("Part 1:", len(paths[(0, 0)]))
    print("Part 2:", max(len(path) for path in paths.values()))


if __name__ == '__main__':
    main(sys.argv[1])
