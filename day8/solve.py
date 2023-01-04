#! /usr/bin/python3
import os, sys
MYDIR = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(MYDIR))
import intcode


def parse_input(path, width, height):
    data = open(path).read().strip()
    layer_bytes = width * height
    layers = []
    while data:
        layer_data, data = data[:layer_bytes], data[layer_bytes:]
        layer = []
        while layer_data:
            row_data, layer_data = layer_data[:width], layer_data[width:]
            layer.append(row_data)
        layers.append(layer)
    return layers


def count_digits(layer):
    digits = {}
    for row in layer:
        for char in row:
            digits[char] = digits.get(char, 0) + 1
    return digits


def render_layers(layers):
    w, h = len(layers[0][0]), len(layers[0])
    result = [[' ' for _ in range(w)] for _ in range(h)]
    done = set()
    for layer in layers:
        for y, row in enumerate(layer):
            for x, cell in enumerate(row):
                if cell == '2' or (x, y) in done:
                    continue
                done.add((x, y))
                if cell == '1':
                    result[y][x] = '█'
        if len(done) == w * h:
            break
    assert len(done) == w * h, len(done)
    return result


def main(input_file):
    layers = parse_input(input_file, 25, 6)
    counts = [count_digits(layer) for layer in layers]
    counts.sort(key=lambda x:x.get('0', 0))
    print("Part 1:", counts[0]['1'] * counts[0]['2'])

    image = render_layers(layers)
    print("Part 2:")
    print('\n'.join(''.join(row) for row in image))


if __name__ == '__main__':
    main(sys.argv[1])
