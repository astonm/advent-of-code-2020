from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return re.findall("e|se|sw|w|nw|ne", line)


# using cube coordinates a la https://www.redblobgames.com/grids/hexagons/
DIRS = {
    "e": Vector([1, -1, 0]),
    "se": Vector([0, -1, 1]),
    "sw": Vector([-1, 0, 1]),
    "w": Vector([-1, 1, 0]),
    "nw": Vector([0, 1, -1]),
    "ne": Vector([1, 0, -1]),
}


def common(input):
    data = [process_line(l) for l in read_file(input)]
    grid = defaultdict(lambda: 1)
    for path in data:
        curr = Vector([0, 0, 0])
        for step in path:
            curr = curr + DIRS[step]

        curr = tuple(curr)
        grid[curr] = 1 - grid[curr]

    return grid


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = common(input)
    print(Counter(grid.values())[0])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = common(input)
    for day in range(1, 101):
        new_grid = defaultdict(lambda: 1)

        ranges = [
            range(min(x[i] for x in grid) - 1, max(x[i] for x in grid) + 2)
            for i in [0, 1, 2]
        ]

        for tile in product(*ranges):
            if tile[0] + tile[1] + tile[2] != 0:
                continue

            new_grid[tile] = grid[tile]
            adj = Counter(grid[tuple(Vector(tile) + d)] for d in DIRS.values())

            if grid[tile] == 0:
                if adj[0] == 0 or adj[0] > 2:
                    new_grid[tile] = 1
            if grid[tile] == 1:
                if adj[0] == 2:
                    new_grid[tile] = 0

        grid = new_grid
        black_tiles = Counter(grid.values())[0]
        print(f"Day {day}: {black_tiles}")


if __name__ == "__main__":
    cli()
