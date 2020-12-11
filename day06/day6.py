import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    out = 0
    for group in groups(input.read()):
        answers = set()
        for row in group:
            for q in row:
                answers.add(q)
        out += len(answers)
    print(out)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    out = 0
    for group in groups(input.read()):
        got = set(group[0])
        for row in group[1:]:
            got = got & set(row)
        out += len(got)
    print(out)


def groups(text):
    return [[q.strip() for q in g.strip().split("\n")] for g in text.split("\n\n")]


if __name__ == "__main__":
    cli()
