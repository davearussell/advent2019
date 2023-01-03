#! /usr/bin/python3
import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def ancestors(self):
        ancestors = []
        node = self
        while (node := node.parent):
            ancestors.append(node)
        return ancestors

    def neighbours(self):
        neighbours = set(self.children)
        if self.parent:
            neighbours.add(self.parent)
        return neighbours


def parse_input(path):
    nodes = {}
    for line in open(path):
        parent_name, child_name = line.strip().split(')')
        parent = nodes.setdefault(parent_name, Node(parent_name))
        child = nodes.setdefault(child_name, Node(child_name))
        parent.children.append(child)
        child.parent = parent
    return nodes


def path_length(src, dst):
    visited = set()
    frontier = {src}
    distance = 0
    while True:
        if dst in frontier:
            return distance
        visited |= frontier
        frontier = {y for x in frontier for y in x.neighbours()} - visited
        distance += 1


def main(input_file):
    nodes = parse_input(input_file)
    orbits = sum(len(node.ancestors()) for node in nodes.values())
    print("Part 1:", orbits)
    print("Part 2:", path_length(nodes['YOU'], nodes['SAN']) - 2)


if __name__ == '__main__':
    main(sys.argv[1])
