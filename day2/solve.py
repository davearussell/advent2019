#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def run(mem, noun, verb):
    mem = mem.copy()
    mem[1] = noun
    mem[2] = verb
    intcode.run(mem)
    return mem[0]


def main(input_file):
    mem = intcode.load(input_file)
    print("Part 1:", run(mem, 12, 2))

    zero_value = run(mem, 0, 0)
    noun_delta = run(mem, 1, 0) - zero_value
    verb_delta = run(mem, 0, 1) - zero_value
    assert verb_delta == 1
    target_value = 19690720
    noun_value, verb_value = divmod(target_value - zero_value, noun_delta)
    print(noun_value * 100 + verb_value)


if __name__ == '__main__':
    main(sys.argv[1])
