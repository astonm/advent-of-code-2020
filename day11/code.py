from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return list(line.strip())


around = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, -1),
    (1, 1),
    (-1, 1),
    (1, -1),
]


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    g = Grid(data)

    def count_visible(grid, x, y):
        s = 0
        for direction in around:
            if grid.get(x + direction[0], y + direction[1], None) == "#":
                s += 1
        return s

    while True:
        next_g = g.copy()

        for y in range(g.height):
            for x in range(g.width):
                if g.get(x, y) == "L" and count_visible(g, x, y) == 0:
                    next_g.set(x, y, "#")

                if g.get(x, y) == "#" and count_visible(g, x, y) >= 4:
                    next_g.set(x, y, "L")

        if g == next_g:
            print(sum(x == "#" for x in g.walk()))
            return
        else:
            g = next_g


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    g = Grid(data)

    last = None

    def find_visible(grid, x, y, direction):
        while True:
            x += direction[0]
            y += direction[1]
            got = grid.get(x, y, None)
            if got not in (".", "#"):
                break
            if got == "#":
                return (x, y)

    def count_visible(grid, x, y):
        s = 0
        for direction in around:
            got = find_visible(grid, x, y, direction)
            if got:
                s += 1
        return s

    while True:
        next_g = g.copy()

        for y in range(g.height):
            for x in range(g.width):
                if g.get(x, y) == "L" and count_visible(g, x, y) == 0:
                    next_g.set(x, y, "#")

                if g.get(x, y) == "#" and count_visible(g, x, y) >= 5:
                    next_g.set(x, y, "L")

        if g == next_g:
            print(sum(x == "#" for x in g.walk()))
            return
        else:
            g = next_g


if __name__ == "__main__":
    cli()
