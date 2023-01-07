#! /usr/bin/python3
import sys


def parse_item(item):
    quantity, material = item.split()
    return int(quantity), material


def parse_input(path):
    recipes = {}
    for line in open(path):
        lhs, rhs = line.split(' => ')
        inputs = [parse_item(item) for item in lhs.split(',')]
        out_n, out_mat = parse_item(rhs)
        recipes[out_mat] = (out_n, inputs)
    return recipes


def manufacture(n, mat, recipes, stock):
    if mat == 'ORE':
        return n
    out_n, inputs = recipes[mat]
    n_runs, rem = divmod(n, out_n)
    if rem:
        n_runs += 1
        stock[mat] = stock.get(mat, 0) + (out_n - rem)
    cost = 0
    for in_n, in_mat in inputs:
        req = in_n * n_runs
        if in_mat in stock:
            if stock[in_mat] >= req:
                stock[in_mat] -= req
                continue
            req -= stock.pop(in_mat)
        cost += manufacture(req, in_mat, recipes, stock)
    return cost


def main(input_file):
    recipes = parse_input(input_file)

    ore_per_fuel = manufacture(1, 'FUEL', recipes, {})
    print("Part 1:", ore_per_fuel)

    ore_count = 10 ** 12
    fuel_count = ore_count // ore_per_fuel
    while (ore_cost := manufacture(fuel_count, 'FUEL', recipes, {})) <= ore_count:
        leftover_ore = ore_count - ore_cost
        fuel_count += max(1, leftover_ore // ore_per_fuel)
    print("Part 2:", fuel_count - 1)


if __name__ == '__main__':
    main(sys.argv[1])
