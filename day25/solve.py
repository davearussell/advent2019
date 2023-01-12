#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode

OPPOSITE = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


def parse_status(text):
    parsed = {'neighbours': {}}
    state = 'room'
    for line in text.split('\n'):
        if not line:
            continue
        if line.startswith('=='):
            assert state == 'room'
            parsed['room'] = line[3:-3]
            state = 'desc'
        elif line == 'Doors here lead:':
            state = 'doors'
        elif line == 'Items here:':
            state = 'items'
        elif line == 'Command?':
            break
        elif state == 'desc':
            parsed['desc'] = parsed.get('desc', '') + line
        elif state in ['doors', 'items']:
            parsed.setdefault(state, []).append(line[2:])
        else:
            raise Exception(text)
    return parsed


def find_path(rooms, src, dst):
    done = set()
    path = {}
    frontier = {dst}
    while frontier:
        new_frontier = set()
        for pos in frontier:
            if pos == src:
                at = src
                steps = []
                while at != dst:
                    steps.append(path[at])
                    at = rooms[at]['neighbours'][path[at]]
                return steps
            for direction, new_pos in rooms[pos]['neighbours'].items():
                if new_pos in done:
                    continue
                done.add(new_pos)
                path[new_pos] = OPPOSITE[direction]
                new_frontier.add(new_pos)
        frontier = new_frontier


def issue_command(proc, cmd, parse=True, **kwargs):
    proc.run(cmd + '\n', **kwargs)
    status_text = proc.read_stdout()
    return parse_status(status_text) if parse else status_text


def navigate_to(proc, rooms, pos, target):
    for step in find_path(rooms, pos, target):
        status = issue_command(proc, step)
    return target


def explore(proc):
    proc.run()
    status = parse_status(proc.read_stdout())
    pos = status['room']
    rooms = {pos: status}
    todo = [(pos, door) for door in status['doors']]

    print("Now at %(room)r, exits are %(doors)s" % status)
    while todo:
        target_room, direction = todo.pop()
        print("Exploring %s from %r" % (direction, target_room))
        pos = navigate_to(proc, rooms, pos, target_room)

        status = issue_command(proc, direction)
        new_pos = status['room']
        print("Now at %(room)r, exits are %(doors)s" % status)
        assert new_pos not in rooms
        rooms[new_pos] = status
        rooms[pos]['neighbours'][direction] = new_pos
        rooms[new_pos]['neighbours'][OPPOSITE[direction]] = pos
        pos = new_pos

        for door in status['doors']:
            if door == OPPOSITE[direction]:
                continue
            elif 'verify your identity' in status['desc']:
                status['sensor'] = direction
            else:
                todo.append((pos, door))

    return rooms, pos


def item_is_safe(proc, rooms, pos, item):
    assert item in rooms[pos].get('items', [])
    tmp = proc.clone()
    try:
        issue_command(tmp, 'take ' + item, parse=False, timeout=1)
        direction = list(rooms[pos]['neighbours'].keys())[0]
        status = issue_command(tmp, direction,)
        if status['room'] != rooms[pos]['neighbours'][direction]:
            raise Exception("Stuck")
    except:
        return False
    return True


def collect_items(proc, rooms, pos):
    items = []
    for room, status in rooms.items():
        if status.get('items'):
            pos = navigate_to(proc, rooms, pos, room)
            for item in status['items']:
                if item_is_safe(proc, rooms, pos, item):
                    issue_command(proc, 'take ' + item, parse=False)
                    items.append(item)
                    print("Taking", item, "from", pos)
                else:
                    print("Cannot take", item, "from", pos)
    return pos, items


def trick_sensor(proc, rooms, pos, items):
    target = [room for room in rooms.values() if 'sensor' in room][0]
    navigate_to(proc, rooms, pos, target['room'])
    have_items = set(items)
    for x in range(1 << len(items)):
        want_items = {item for (i, item) in enumerate(items) if x & (1 << i)}
        for item in want_items - have_items:
            issue_command(proc, 'take ' + item, parse=False)
        for item in have_items - want_items:
            issue_command(proc, 'drop ' + item, parse=False)
        have_items = want_items
        result = issue_command(proc, target['sensor'], parse=False)
        if 'ejected' not in result:
            print("Passed sensor with:", ', '.join(have_items))
            print(result)
            break


def main(input_file):
    proc = intcode.Process(intcode.load(input_file))
    print(" ======== Exploring rooms ========")
    rooms,  pos = explore(proc)
    print(" ======== Collecting items ========")
    pos, items = collect_items(proc, rooms, pos)
    print(" ======== Brute-forcing sensor ========")
    trick_sensor(proc, rooms, pos, items)


if __name__ == '__main__':
    main(sys.argv[1])
