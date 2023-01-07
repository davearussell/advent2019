#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def render_grid(grid, score):
    maxx = max(x for (x, y) in grid)
    minx = min(x for (x, y) in grid)
    maxy = max(y for (x, y) in grid)
    miny = min(y for (x, y) in grid)
    rendered = 'Score: %d\n' % (score,)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            v = grid.get((x, y), 0)
            rendered += {0: ' ', 1: '█', 2: '#', 3: '-', 4: '*'}[v]
        rendered += '\n'
    return rendered


def signsub(a, b):
    return int(a > b) - int(a < b)


def play(mem):
    proc = intcode.Process(mem)
    grid = {}
    score = 0
    while True:
        proc.run()
        while proc.outputs:
            x, y, v = [proc.outputs.pop(0) for _ in range(3)]
            if (x, y) == (-1, 0):
                score = v
            else:
                grid[(x, y)] = v
        print('\x1b[;H\x1b[J' + render_grid(grid, score))
        if proc.state == 'done':
            break
        ball = [p for p in grid if grid[p] == 4][0]
        paddle = [p for p in grid if grid[p] == 3][0]
        proc.run(signsub(ball[0], paddle[0]))
    return grid, score


def main(input_file):
    mem = intcode.load(input_file)
    p1_grid, p1_score = play(mem.copy())
    mem[0] = 2
    p2_grid, p2_score = play(mem)
    print("Part 1:", list(p1_grid.values()).count(2))
    print("Part 2:", p2_score)


if __name__ == '__main__':
    main(sys.argv[1])
