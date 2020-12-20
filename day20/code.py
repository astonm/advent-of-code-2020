from util import *


@click.group()
def cli():
    pass


def process_line(line):
    lines = line.split("\n")
    [name] = parse("Tile {:d}:", lines[0])

    tile = [[l for l in q] for q in lines[1:]]
    return Tile(name, Grid(tile))


class Tile:
    def __init__(self, name, grid, skip_sides=False):
        self.name = name
        self.grid = grid
        self._orientations = []

        size = self.grid.width
        if not skip_sides:
            self.sides = [
                "".join([self.grid.get(x, 0) for x in range(size)]),
                "".join([self.grid.get(size - 1, y) for y in range(size)]),
                "".join([self.grid.get(x, size - 1) for x in range(size)]),
                "".join([self.grid.get(0, y) for y in range(size)]),
            ]

    def flip_horiz(self):
        flipped = self.grid.copy()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                other = self.grid.get(self.grid.width - 1 - x, y)
                flipped.set(x, y, other)
        return Tile(self.name, flipped)

    def flip_vert(self):
        flipped = self.grid.copy()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                other = self.grid.get(x, self.grid.height - 1 - y)
                flipped.set(x, y, other)
        return Tile(self.name, flipped)

    def rotate90(self):
        rotated = self.grid.copy()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                other = self.grid.get(y, self.grid.width - 1 - x)
                rotated.set(x, y, other)
        return Tile(self.name, rotated)

    @cached_property
    def all_orientations(self):
        out = []

        o = self
        for _ in range(4):
            out.append(o)
            o = o.rotate90()

        o = o.flip_horiz()
        for _ in range(4):
            o = o.rotate90()
            out.append(o)
        o = o.flip_horiz()

        o = o.flip_vert()
        for _ in range(4):
            o = o.rotate90()
            out.append(o)

        return out


def print_tile(t):
    print(t.sides[0])
    for h in range(1, 9):
        print(t.sides[3][h] + f"{t.name:^8}" + t.sides[1][h])
    print(t.sides[2])


def print_board_outlines(so_far, size):
    for row in range(size):
        this_row = so_far[size * row : size * row + size]
        print("|".join([t.sides[0] for t in this_row]))
        for h in range(1, 9):
            print("|".join([t.sides[3][h] + " " * 8 + t.sides[1][h] for t in this_row]))
        print("|".join([t.sides[2] for t in this_row]))


def image_lines(tiles, size):
    def t_grid_line(tile, line_index):
        return [tile.grid.get(i, line_index) for i in range(1, 9)]

    out = []
    for row in range(size):
        this_row = tiles[size * row : size * row + size]
        for i in range(1, 9):
            temp = []
            for t in this_row:
                temp.extend(t_grid_line(t, i))
            out.append(temp)
    return out


def solve(tiles, size):
    by_name = {t.name: t for t in tiles}

    def _solve(so_far, to_place):
        if not to_place:
            return so_far

        i = len(so_far)
        for name in to_place:
            for o in by_name[name].all_orientations:
                okay = True
                if i % size > 0:  # not left edge
                    if so_far[i - 1].sides[1] != o.sides[3]:
                        okay = False
                if i >= size:  # not top edge
                    if so_far[i - size].sides[2] != o.sides[0]:
                        okay = False

                if okay:
                    n_so_far = so_far + [o]
                    n_to_place = set(to_place) - {o.name}
                    res = _solve(n_so_far, n_to_place)
                    if res:
                        return res

    return _solve([], set(by_name))


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    tiles = [process_line(l) for l in read_file(input, delim="\n\n")]
    size = int(len(tiles) ** 0.5)
    out = solve(tiles, size)
    print(out[0].name * out[size - 1].name * out[-size].name * out[-1].name)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    tiles = [process_line(l) for l in read_file(input, delim="\n\n")]
    size = int(len(tiles) ** 0.5)
    out = solve(tiles, size)

    final = Tile("image", Grid(image_lines(out, size)))
    for i, o in enumerate(final.all_orientations):
        c = 0
        for x in range(o.grid.width):
            for y in range(o.grid.width):
                missed = False
                for (dx, dy) in MONSTER:
                    if o.grid.get(x + dx, y + dy, default=".") != "#":
                        missed = True
                        break
                if not missed:
                    c += 1
                    for (dx, dy) in MONSTER:
                        o.grid.set(x + dx, y + dy, "O")
        if c:
            o.grid.print()
            print(f"orientation {i=}, found {c=}")
            print(len([x for x in o.grid.walk() if x == "#"]))


MONSTER = [
    (0, 18),
    (1, 0),
    (1, 5),
    (1, 6),
    (1, 11),
    (1, 12),
    (1, 17),
    (1, 18),
    (1, 19),
    (2, 1),
    (2, 4),
    (2, 7),
    (2, 10),
    (2, 13),
    (2, 16),
]


if __name__ == "__main__":
    cli()
