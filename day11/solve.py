#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def paint_grid(mem, grid):
    proc = intcode.Process(mem)
    pos = (0, 0)
    facing = 0
    vectors = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
    while proc.state != 'done':
        current_color = grid.get(pos, 0)
        proc.run(current_color)
        new_color = proc.outputs.pop(0)
        turn = proc.outputs.pop(0)
        grid[pos] = new_color

        facing = (facing + (1 if turn else -1)) % 4
        dx, dy = vectors[facing]
        pos = (pos[0] + dx, pos[1] + dy)
    return grid


def render_grid(grid):
    minx = min(x for (x, y), v in grid.items() if v)
    maxx = max(x for (x, y), v in grid.items() if v)
    miny = min(y for (x, y), v in grid.items() if v)
    maxy = max(y for (x, y), v in grid.items() if v)

    s = ''
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            s += '█' if grid.get((x, y)) else ' '
        s += '\n'
    return s


def main(input_file):
    mem = intcode.load(input_file)
    print("Part 1:", len(paint_grid(mem.copy(), {})))
    print("Part 2:\n" + render_grid(paint_grid(mem.copy(), {(0, 0): 1})))


if __name__ == '__main__':
    main(sys.argv[1])
