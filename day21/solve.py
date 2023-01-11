#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def go(mem, cmds):
    proc = intcode.Process(mem)
    proc.run('\n'.join(cmds) + '\n')
    if proc.outputs[-1] < 256:
        print(proc.read_stdout())
        return None
    else:
        return proc.outputs[-1]


def main(input_file):
    mem = intcode.load(input_file)

    part1_cmds = [
        'NOT A J',  # j = !a
        'NOT J J',  # j = a
        'AND B J',  # j = a & b
        'AND C J',  # j = a & b & c
        'NOT J J',  # j = !(a & b & c)
        'AND D J',  # j = d & !(a & b & c)
        'WALK',
    ]
    print("Part 1:", go(mem.copy(), part1_cmds))

    part2_cmds = part1_cmds[:-1] + [
        'NOT E T',  # t = !e
        'NOT T T',  # t = e
        'OR H T',   # t = e | h
        'AND T J',  # j = d & !(a & b & c) & (e | h)
        'RUN',
    ]
    print("Part 2:", go(mem.copy(), part2_cmds))


if __name__ == '__main__':
    main(sys.argv[1])
