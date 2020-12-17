from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


def ranges(g, dims=3, extend_by=0):
    mins = [min(g, key=lambda x: x[i])[i] for i in range(dims)]
    maxs = [max(g, key=lambda x: x[i])[i] for i in range(dims)]

    return [range(mins[i] - extend_by, maxs[i] + extend_by + 1) for i in range(dims)]


def printg(g):
    xr, yr, zr = ranges(g)
    for z in zr:
        for y in yr:
            for x in xr:
                print(g[(x, y, z)], sep="", end="")
            print()
        print()


def ncount(g, p, dims=3):
    c = 0
    for d in product([-1, 0, 1], repeat=dims):
        if all(x == 0 for x in d):
            continue
        np = tuple(x + dx for (x, dx) in zip(p, d))
        c += int(g.get(np) == "#")
    return c


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    g = {}
    for y, line in enumerate(read_file(input)):
        for x, c in enumerate(line):
            g[(x, y, 0)] = c

    for _ in range(6):
        # printg(g)
        # print("------")
        ng = g.copy()
        xr, yr, zr = ranges(g, extend_by=1)
        for z in zr:
            for y in yr:
                for x in xr:
                    p = (x, y, z)
                    if g.get(p) == "#":
                        ng[p] = "#" if ncount(g, p) in (2, 3) else "."
                    else:
                        ng[p] = "#" if ncount(g, p) == 3 else "."
        g = ng

    print(sum(v == "#" for v in g.values()))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    g = {}
    for y, line in enumerate(read_file(input)):
        for x, c in enumerate(line):
            g[(x, y, 0, 0)] = c

    for _ in range(6):
        ng = g.copy()
        xr, yr, zr, wr = ranges(g, dims=4, extend_by=1)
        for w in wr:
            for z in zr:
                for y in yr:
                    for x in xr:
                        p = (x, y, z, w)
                        if g.get(p) == "#":
                            ng[p] = "#" if ncount(g, p, dims=4) in (2, 3) else "."
                        else:
                            ng[p] = "#" if ncount(g, p, dims=4) == 3 else "."
        g = ng

    print(sum(v == "#" for v in g.values()))


@cli.command()
@click.argument("input", type=click.File())
def part3(input):
    g = GridN(default=".")
    for y, line in enumerate(read_file(input)):
        for x, c in enumerate(line):
            g.set((x, y, 0), c)

    for _ in range(6):
        # g.print()
        ng = g.copy()
        for p, val in g.walk_all(pad=1):
            nearby_actives = [n for n in g.neighbors(p, diags=True) if n[1] == "#"]
            if val == "#":
                ng.set(p, "#" if len(nearby_actives) in (2, 3) else ".")
            else:
                ng.set(p, "#" if len(nearby_actives) == 3 else ".")
        g = ng

    print(sum(v == "#" for _, v in g.walk()))


if __name__ == "__main__":
    cli()
