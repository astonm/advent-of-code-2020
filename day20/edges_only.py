from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return Tile.from_line(line)


def side(cs):
    return "".join(cs)


class Tile:
    def __init__(self):
        self.name = None
        self.sides = []

    def from_line(text):
        out = Tile()
        lines = text.split("\n")
        [out.name] = parse("Tile {:d}:", lines[0])
        grid = Grid(lines[1:])
        out.sides = [
            side([grid.get(x, 0) for x in range(10)]),
            side([grid.get(9, y) for y in range(10)]),
            side([grid.get(x, 9) for x in range(10)]),
            side([grid.get(0, y) for y in range(10)]),
        ]
        return out

    def flip_horiz(self):
        out = Tile()
        out.name = self.name
        out.sides = [
            self.sides[0][::-1],
            self.sides[3],
            self.sides[2][::-1],
            self.sides[1],
        ]

        return out

    def flip_vert(self):
        out = Tile()
        out.name = self.name
        out.sides = [
            self.sides[2],
            self.sides[1][::-1],
            self.sides[0],
            self.sides[3][::-1],
        ]
        return out

    def rotate90(self):
        out = Tile()
        out.name = self.name
        out.sides = [
            self.sides[3][::-1],
            self.sides[0],
            self.sides[1][::-1],
            self.sides[2],
        ]
        return out

    def all_orientations(self):
        o = self

        for _ in range(4):
            yield o
            o = o.rotate90()

        o = o.flip_horiz()
        for _ in range(4):
            o = o.rotate90()
            yield o
        o = o.flip_horiz()

        o = o.flip_vert()
        for _ in range(4):
            o = o.rotate90()
            yield o


def print_tile(t):
    print(t.sides[0])
    for h in range(1, 9):
        print(t.sides[3][h] + f"{t.name:^8}" + t.sides[1][h])
    print(t.sides[2])


def print_board(so_far, size):
    for row in range(size):
        this_row = so_far[size * row : size * row + size]
        print("|".join([t.sides[0] for t in this_row]))
        for h in range(1, 9):
            print("|".join([t.sides[3][h] + " " * 8 + t.sides[1][h] for t in this_row]))
        print("|".join([t.sides[2] for t in this_row]))


def image_lines(tiles, size):
    out = []
    for row in range(size):
        this_row = tiles[size * row : size * row + size]
        out.append("".join([t.sides[0] for t in this_row]))
        for h in range(1, 9):
            out.append(
                "".join([t.sides[3][h] + " " * 8 + t.sides[1][h] for t in this_row])
            )
        out.append("".join([t.sides[2] for t in this_row]))
    return out


def solve(tiles, size):
    by_name = {t.name: t for t in tiles}

    def _solve(so_far, to_place):
        if not to_place:
            return so_far

        i = len(so_far)
        for name in to_place:
            for o in by_name[name].all_orientations():
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
    pprint(image_lines(out, size))
    print()


if __name__ == "__main__":
    cli()
