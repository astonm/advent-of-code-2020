import click


@click.group()
def cli():
    pass


def pass_to_id(s):
    return row(s[:-3]) * 8 + col(s[-3:])


def row(s):
    return int(s.replace("F", "0").replace("B", "1"), 2)


def col(s):
    return int(s.replace("L", "0").replace("R", "1"), 2)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    print(max(pass_to_id(p.strip()) for p in input))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    ids = sorted(pass_to_id(p.strip()) for p in input)
    last_id = -100
    for id in ids:
        if id - last_id == 2:
            print(last_id + 1)
        last_id = id


if __name__ == "__main__":
    cli()
