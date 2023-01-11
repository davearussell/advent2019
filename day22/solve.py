#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode

# 0: x
# 1: x + C1
# 2: C2 - x
# 3: C3 - C4 * x
# 4: C5 - C4 * x
# ...
# End results will be a big polynomial in x

# Can you relate ((X ^ n) MOD Y) to (X mod Y) ?
# Note Y is prime
# (X ^ (Y - 1)) MOD Y == 1, but I don't think this helps


def parse_input(path):
    ops = []
    for line in open(path):
        words = line.split()
        if words[1] == 'into':
            ops.append(('reverse', None))
        else:
            ops.append((words[0], int(words[-1])))
    return ops


def shuffle(ops, pos, n_cards):
    for op, arg in ops:
        if op == 'reverse':
            pos = n_cards - pos - 1
        elif op == 'deal':
            pos = (pos * arg) % n_cards
        else: # cut
            pos = (pos - arg) % n_cards
    return pos

def modinv(x, m):
    return pow(x, -1, m)


def rev_shuffle(ops, pos, n_cards):
    for op, arg, in ops[::-1]:
        if op == 'reverse':
            pos = n_cards - pos - 1
        elif op == 'deal':
            pos = (pos * modinv(arg, n_cards)) % n_cards
        else:
            pos = (pos + arg) % n_cards
    return pos


def main(input_file):
    ops = parse_input(input_file)
    print("Part 1:", shuffle(ops, 2019, 10007))

    pos = 2020
    n_cards = 119315717514047
    n_iters = 101741582076661

    # y = ax + b MOD n
    # z = ay + b MOD n
    # y - z = a(x - y) MOD n
    # a = (y - z) / (x - y) MOD n
    # a = (y - z) * inv(x - y) MOD n
    # b = y - ax MOD n
    x = pos
    y = rev_shuffle(ops, x, n_cards)
    z = rev_shuffle(ops, y, n_cards)
    a = ((y - z) * modinv(x - y, n_cards)) % n_cards
    b = (y - a * x) % n_cards

    # f(x)    = ax + b
    # f^2(x)  = a(ax + b) + b
    #         = aax + ab + b
    # f^3(x)  = a(aax + ab + b) + b
    #         = aaax + aab + ab + b
    # f^n(x)  = a^n * x + sum(c=0...n-1)(a^c * b)
    #         = a^n * x + (a^n - 1) / (a - 1) * b
    result = (
        pow(a, n_iters, n_cards) * x +
        (pow(a, n_iters, n_cards) - 1) * modinv(a - 1, n_cards) * b
    ) % n_cards
    print("Part 2:", result)


if __name__ == '__main__':
    main(sys.argv[1])
