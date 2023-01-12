#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def main(input_file):
    mem = intcode.load(input_file)
    procs = [intcode.Process(mem.copy(), [i]) for i in range(50)]
    pkts = {}
    last_nat = None

    while True:
        idle = True
        for addr, proc in enumerate(procs):
            proc.run(pkts.pop(addr, [-1]))
            while proc.outputs:
                idle = False
                addr, x, y = [proc.outputs.pop(0) for _ in range(3)]
                if addr == 255:
                    if addr in pkts:
                        if pkts[addr][1] == y:
                            print("Part 2:", y)
                            return
                    else:
                        print("Part 1:", y)
                    pkts[addr] = [x, y]
                else:
                    pkts.setdefault(addr, []).extend([x, y])
        if idle:
            pkts[0] = pkts[255].copy()


if __name__ == '__main__':
    main(sys.argv[1])
