#! /usr/bin/python3
import os, sys
import itertools

MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def run_all(procs):
    alive = True
    while alive:
        alive = False
        for i, proc in enumerate(procs):
            if proc.state != 'done':
                alive = True
                proc.run()
                if proc.outputs:
                    procs[(i + 1) % len(procs)].inputs += proc.outputs
                    proc.outputs.clear()


def try_phase_order(phase_order, prog):
    procs = [intcode.Process(prog.copy(), [phase])
             for i, phase in enumerate(phase_order)]
    procs[0].inputs += [0]
    run_all(procs)
    return procs[0].inputs[-1]


def try_all_orders(prog, phases):
    scores = [
        try_phase_order(phase_order, prog)
        for phase_order in itertools.permutations(phases)
    ]
    return max(scores)


def main(input_file):
    prog = intcode.load(input_file)
    print("Part 1:", try_all_orders(prog, [0, 1, 2, 3, 4]))
    print("Part 2:", try_all_orders(prog, [5, 6, 7, 8, 9]))


if __name__ == '__main__':
    main(sys.argv[1])
