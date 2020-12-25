from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


MAGIC = 20201227


def transform(n, target=None, loop_size=None):
    if target:
        loop_size = inf
    p = 1
    i = 0
    while i < loop_size:
        i += 1
        p *= n
        p = p % MAGIC
        if p == target:
            return i
    return p


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    card_key, door_key = [process_line(l) for l in read_file(input)]
    cl = transform(7, target=card_key)
    dl = transform(7, target=door_key)

    guess1 = transform(door_key, loop_size=cl)
    guess2 = transform(card_key, loop_size=dl)

    assert guess1 == guess2
    pprint(guess2)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    print("🦌 🌟")


if __name__ == "__main__":
    cli()
