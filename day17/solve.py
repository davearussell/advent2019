#! /usr/bin/python3
import os, sys, copy
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


OFFSETS = {'n': (0, -1), 'e': (1, 0), 's': (0, 1), 'w': (-1, 0)}
CLOCKWISE = {'n': 'e', 'e': 's', 's': 'w', 'w': 'n'}
ANTICLOCKWISE = {v: k for (k, v) in CLOCKWISE.items()}


def load_grid(mem):
    text = ''.join(map(chr, intcode.run(mem.copy()))).strip()
    grid = set()
    robot = None
    for y, row in enumerate(text.split('\n')):
        for x, cell in enumerate(row):
            if cell != '.':
                grid.add((x, y))
                if cell != '#':
                    direction = {'^': 'n', '>': 'e', 'v': 's', '<': 'w'}[cell]
                    robot = ((x, y), direction)
    return grid, robot


def move(pos, direction):
    x, y = OFFSETS[direction]
    return (pos[0] + x, pos[1] + y)


def valid_directions(grid, pos):
    return {direction for direction in OFFSETS if move(pos, direction) in grid}


def find_junctions(grid):
    return {pos for pos in grid if len(valid_directions(grid, pos)) > 2}


def plot_path(grid, robot_pos, direction):
    path = []
    while True:
        directions = valid_directions(grid, robot_pos)
        if direction not in directions:
            if CLOCKWISE[direction] in directions:
                path += ['R', 0]
                direction = CLOCKWISE[direction]
            elif ANTICLOCKWISE[direction] in directions:
                path += ['L', 0]
                direction = ANTICLOCKWISE[direction]
            else: # can't go straight, left, or right: we've hit the end
                break
        robot_pos = move(robot_pos, direction)
        path[-1] += 1
    return [str(x) for x in path]


def try_split(path, routines, calls):
    if len(','.join(calls)) > 20:
        return False, routines, calls
    if not path:
        return True, routines, calls
    for x, routine in zip('ABC', routines):
        n = len(routine)
        if path[:n] == routine:
            ok, _routines, _calls = try_split(path[n:], routines, calls + [x])
            if ok:
                return ok, _routines, _calls
    if len(routines) < 3:
        n = 2
        x = 'ABC'[len(routines)]
        while len(','.join(routine := path[:n])) <= 20:
            ok, _routines, _calls = try_split(path[n:], routines + [routine], calls + [x])
            if ok:
                return ok, _routines, _calls
            n += 2
    return False, routines, calls


def split_path(path):
    ok, routines, calls = try_split(path, [], [])
    if not ok:
        raise Exception("No valid splits found for path")
    return routines, calls


def answer_prompt(proc, prompt, answer):
    proc.run()
    output_text = proc.read_stdout()
    if not output_text.endswith(prompt + '\n'):
        raise Exception("Did not see %r" % (prompt,))
    proc.run(answer + '\n')


def run_robot(mem, routines, calls):
    mem[0] = 2
    proc = intcode.Process(mem)
    answer_prompt(proc, 'Main:', ','.join(calls))
    for x, routine in zip('ABC', routines):
        answer_prompt(proc, 'Function %s:' % (x,), ','.join(routine))
    answer_prompt(proc, 'Continuous video feed?', 'n')
    return proc.outputs[-1]


def main(input_file):
    mem = intcode.load(input_file)
    grid, (robot, direction) = load_grid(mem)
    print("Part 1:", sum(x * y for (x, y) in find_junctions(grid)))

    # Part 2 assumptions:
    # 1. The grid contains no T junctions, only 4-way intersections
    # 2. The grid is setup such that you will cover every cell if you
    #    move forward whever possible, and turn otherwise (the lack of
    #    T junctions ensures there is never a choice of turn direction)
    # 3. There exists a solution that takes the above path
    # 4. The three movement routines align to the above path, i.e. we
    #    never have to split a segment of straight-line movement across
    #    two routines.
    path = plot_path(grid, robot, direction)
    routines, calls = split_path(path)
    print("Part 2:", run_robot(mem, routines, calls))


if __name__ == '__main__':
    main(sys.argv[1])
