#! /usr/bin/python3
import sys


def parse_input(path):
    pathable = set()
    keys = {}
    doors = {}
    robots = []
    for y, line in enumerate(open(path)):
        for x, char in enumerate(line.strip()):
            if char != '#':
                pathable.add((x, y))
                if char == '@':
                    robots.append((x, y))
                elif char.islower():
                    keys[char] = (x, y)
                elif char.isupper():
                    doors[char.lower()] = (x, y)
    return pathable, keys, doors, robots


def path_costs(pathable, pos, keys, doors):
    revdoors = {pos: x for x, pos in doors.items()}
    costs = {} # pos -> (dist, doors)
    distance = 0
    frontier = {(pos, '')} # { (pos, doors), ... }
    while frontier:
        new_frontier = set()
        for pos, doors in frontier:
            if pos in revdoors:
                doors = ''.join(sorted(doors + revdoors[pos]))
            costs[pos] = (distance, doors)
            x, y = pos
            neighbours = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
            for neighbour in (neighbours & pathable) - set(costs):
                new_frontier.add( (neighbour, doors) )
        distance += 1
        frontier = new_frontier
    return {key: costs[key_pos] for key, key_pos in keys.items() if key_pos in costs}


def solve(pathable, keys, doors, robots):
    srcs = [(i, robot) for (i, robot) in enumerate(robots)] + list(keys.items())
    paths = {label: path_costs(pathable, src, keys, doors) for label, src in srcs}
    robot_keys = {key: robot for robot in range(len(robots)) for key in paths[robot]}
    all_keys = ''.join(sorted(robot_keys))
    states = {(tuple(range(len(robots))), ''): 0}
    best = None

    while states:
        new_states = {}
        for (robots, have_keys), state_dist in states.items():
            missing_keys = [k for k in all_keys if k not in have_keys]
            for key in missing_keys:
                robot = robot_keys[key]
                robot_pos = robots[robot]
                key_dist, req_keys = paths[robot_pos][key]
                if not all(k in have_keys for k in req_keys):
                    continue
                new_dist = state_dist + key_dist
                new_have_keys = ''.join(sorted(have_keys + key))
                if new_have_keys == all_keys:
                    if best is None or best > new_dist:
                        best = new_dist
                else:
                    new_robots = list(robots)
                    new_robots[robot] = key
                    dictk = (tuple(new_robots), new_have_keys)
                    if dictk not in new_states or new_states[dictk] > new_dist:
                        new_states[dictk] = new_dist
        states = new_states
    return best


def main(input_file):
    pathable, keys, doors, robots = parse_input(input_file)
    assert len(robots) == 1, robots

    print("Part 1:", solve(pathable, keys, doors, robots))

    x, y = robots[0]
    robots = [(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]
    pathable -= {(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
    print("Part 2:", solve(pathable, keys, doors, robots))



if __name__ == '__main__':
    main(sys.argv[1])
