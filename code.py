from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    print()


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    print()


if __name__ == "__main__":
    cli()
