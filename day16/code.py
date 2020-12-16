from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


def rangeof(s):
    x, y = parse("{}-{}", s)
    return int(x), int(y)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    groups = []
    my_ticket = None
    nearby = []

    section = 0
    for line in data:
        if not line:
            section += 1
            continue
        if section == 0:
            group, range1, range2 = parse("{}: {} or {}", line)
            range1, range2 = [rangeof(x) for x in (range1, range2)]
            groups.append((group, range1, range2))
        if section == 1:
            if ":" in line:
                continue
            my_ticket = [int(x) for x in line.split(",")]
        if section == 2:
            if ":" in line:
                continue
            nearby.append([int(x) for x in line.split(",")])

    out = 0
    for tick in nearby:
        for elm in tick:
            if not any(r[0] <= elm <= r[1] for g in groups for r in g[1:]):
                out += elm
    print(out)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    groups = []
    my_ticket = None
    nearby = []

    section = 0
    for line in data:
        if not line:
            section += 1
            continue
        if section == 0:
            group, range1, range2 = parse("{}: {} or {}", line)
            range1, range2 = [rangeof(x) for x in (range1, range2)]
            groups.append((group, (range1, range2)))
        if section == 1:
            if ":" in line:
                continue
            my_ticket = [int(x) for x in line.split(",")]
        if section == 2:
            if ":" in line:
                continue
            nearby.append([int(x) for x in line.split(",")])

    valid = []
    for tick in nearby:
        t = []
        for elm in tick:
            t.append(any(r[0] <= elm <= r[1] for g in groups for r in g[1]))
        if all(t):
            valid.append(tick)

    fields = dict(groups)
    possibles = [set(fields) for i in range(len(valid[0]))]

    for row in valid + [my_ticket]:
        for i, val in enumerate(row):
            matching_fields = set()
            for field, (s, t) in fields.items():
                if s[0] <= val <= s[1] or t[0] <= val <= t[1]:
                    matching_fields.add(field)
            possibles[i] &= matching_fields

    while not all(len(s) == 1 for s in possibles):
        # find a single and nuke from the rest
        ones = [o for o in enumerate(possibles) if len(o[1]) == 1]
        for p in possibles:
            if len(p) > 1:
                for _, one in ones:
                    p -= one

    field_inds = {}
    for i, p in enumerate(possibles):
        field_inds[next(iter(p))] = i

    parts = []
    for field, i in field_inds.items():
        if field.startswith("departure"):
            parts.append(my_ticket[i])
    print(prod(parts))


if __name__ == "__main__":
    cli()
