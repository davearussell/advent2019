#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def get_initial_xs(pull, y):
    """Perform a dumb search for find the range of active x values for
    this y value"""
    x0 = None
    for x in range(y // 5, (y + 1) * 5):
        if pull(x, y):
            if x0 is None:
                x0 = x
        else:
            if x0 is not None:
                return x0, x - 1
    return None, None


def get_xs(pull, y, c0, c1):
    """Use known coefficients to do an efficient search for the active
    x values for this y value"""
    x0 = int(y * c0)
    while not pull(x0, y):
        x0 += 1
        if x0 // y > 5:
            return None, None
    while pull(x0 - 1, y):
        x0 -= 1

    x1 = max(x0, int(y * c1))
    while not pull(x1, y):
        x1 -= 1
    while pull(x1 + 1, y):
        x1 += 1

    return (x0, x1)


def estimate_coefficients(pull, precision=5):
    """The left and right sides of the tractor beam are both lines of
    the form x = cy. Returns estimates for the two c values at the
    specified number of decimal places."""
    y = 10
    x0, x1 = get_initial_xs(pull, y)
    c0 = x0 / 10
    c1 = x1 / 10
    for _ in range(precision):
        y *= 10
        x0, x1 = get_xs(pull, y, c0, c1)
        c0 = x0 / y
        c1 = x1 / y
    return c0, c1


def make_grid(pull, size, c0, c1):
    """Returns the set of active points in the square of this size
    starting at the origin."""
    grid = set()
    for y in range(size):
        x0, x1 = get_xs(pull, y, c0, c1)
        if x0 is not None:
            x1 = min(x1, 49)
            grid |= {(x, y) for x in range(x0, x1 + 1)}
    return grid


def find_square(pull, size, c0, c1):
    """Returns the origin of the first square of the specified size that
    that fits entirely within the beam."""
    # We make a first estimate for y by solving:
    #   x + size == c1 * y
    #   x == c0 * (y + size)
    # Working:
    #   x == c1 * y - size
    #   c0 * (y + size) == c1 * y - size
    #   c0 * y + c0 * size = c1 * y - size
    #   c1 * y - c0 * y = c0 * size + size
    #   y * (c1 - c0) = size * (c0 + 1)
    #   y = (size * (c0 + 1)) / (c1 - c0)
    size -= 1
    est_y = (size * (c0 + 1)) / (c1 - c0)

    y0 = int(est_y) - 10
    while True:
        y1 = y0 + size
        _, x1 = get_xs(pull, y0, c0, c1)
        x0 = x1 - size
        found_x0, _ = get_xs(pull, y1, c0, c1)
        if found_x0 <= x0:
            return x0, y0
        y0 += 1


def main(input_file):
    mem = intcode.load(input_file)
    def pull(x, y):
        return intcode.run(mem.copy(), [x, y]).pop()

    c0, c1 = estimate_coefficients(pull)
    print("Coefficients:", c0, c1)

    grid = make_grid(pull, 50, c0, c1)
    print("Part 1:", len(grid))

    x, y = find_square(pull, 100, c0, c1)
    print("Part 2:", x * 10000 + y)


if __name__ == '__main__':
    main(sys.argv[1])
