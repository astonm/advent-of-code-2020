from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return list(map(int, line.split(",")))


def rfind(l, e):
    for i in range(len(l) - 1, -1, -1):
        if l[i] == e:
            return i
    raise ValueError("oops")


@cli.command()
@click.argument("input", type=click.File())
@click.argument("pos", type=int)
def part1(input, pos):
    data = [process_line(l) for l in read_file(input)][0]
    for i in range(len(data), pos):
        last = data[-1]
        try:
            b = rfind(data[:-1], last)
            data.append(i - b - 1)
        except:
            data.append(0)
    print(data[-1])


@cli.command()
@click.argument("input", type=click.File())
@click.argument("pos", type=int)
def part2(input, pos):
    data = [process_line(l) for l in read_file(input)][0]
    prev_ind = {k: i for (i, k) in enumerate(data)}

    last = data[-1]
    last_ind = -1

    for i in range(len(data), pos):
        if last_ind < 0:
            last = 0
        else:
            last = i - last_ind - 1

        last_ind = prev_ind.get(last, -1)
        prev_ind[last] = i

    print(last)


if __name__ == "__main__":
    cli()
