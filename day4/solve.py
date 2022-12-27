#! /usr/bin/python3
import sys


def main(input_file):
    a, b = [int(x) for x in open(input_file).read().split('-')]

    def is_valid(n, allow_triples):
        digits = [int(c) for c in str(n)]
        a, b, c, d, e, f = digits
        if not a <= b <= c <= d <= e <= f:
            return False
        if allow_triples:
            return any([a == b, b == c, c == d, d == e, e == f])
        else:
            return any([
                a == b != c,
                a != b == c != d,
                b != c == d != e,
                c != d == e != f,
                d != e == f
            ])

    valid1 = [n for n in range(a, b + 1) if is_valid(n, True)]
    print("Part 1:", len(valid1))
            
    valid2 = [n for n in range(a, b + 1) if is_valid(n, False)]
    print("Part 2:", len(valid2))


if __name__ == '__main__':
    main(sys.argv[1])
