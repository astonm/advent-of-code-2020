from util import *


@click.group()
def cli():
    pass


def rotate(x, y, degrees):
    o = degrees / 360 * 2 * pi
    return (
        round(x * cos(o) - y * sin(o)),
        round(y * cos(o) + x * sin(o)),
    )


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    x, y = 0, 0
    dx, dy = 1, 0
    for line in read_file(input):
        d = parse("{dir}{n:d}", line)
        if d["dir"] == "N":
            y -= d["n"]
        if d["dir"] == "S":
            y += d["n"]
        if d["dir"] == "E":
            x += d["n"]
        if d["dir"] == "W":
            x -= d["n"]

        if d["dir"] == "F":
            x += dx * d["n"]
            y += dy * d["n"]

        if d["dir"] == "L":
            dx, dy = rotate(dx, dy, -d["n"])
        if d["dir"] == "R":
            dx, dy = rotate(dx, dy, d["n"])
        print(d, x, y, dx, dy)
    print(abs(x) + abs(y))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    x, y = 0, 0
    dx, dy = 10, -1
    for line in read_file(input):
        d = parse("{dir}{n:d}", line)
        if d["dir"] == "N":
            dy -= d["n"]
        if d["dir"] == "S":
            dy += d["n"]
        if d["dir"] == "E":
            dx += d["n"]
        if d["dir"] == "W":
            dx -= d["n"]

        if d["dir"] == "F":
            x += dx * d["n"]
            y += dy * d["n"]

        if d["dir"] == "L":
            dx, dy = rotate(dx, dy, -d["n"])
        if d["dir"] == "R":
            dx, dy = rotate(dx, dy, d["n"])

        print(d, x, y, dx, dy)
    print(abs(x) + abs(y))


if __name__ == "__main__":
    cli()
