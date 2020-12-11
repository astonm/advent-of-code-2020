import click


@click.group()
def cli():
    pass


def softint(s):
    try:
        return int(s)
    except ValueError:
        return -1


def hgt(x):
    if x.endswith("cm"):
        return 150 <= softint(x[:-2]) <= 193
    if x.endswith("in"):
        return 59 <= softint(x[:-2]) <= 76


def hcl(x):
    if x.startswith("#") and len(x) == 7:
        try:
            int(x[1:], 16)
            return True
        except:
            return False


ALL_FIELDS = {
    "byr": lambda x: 1920 <= softint(x) <= 2002,
    "iyr": lambda x: 2010 <= softint(x) <= 2020,
    "eyr": lambda x: 2020 <= softint(x) <= 2030,
    "hgt": hgt,
    "hcl": hcl,
    "ecl": lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
    "pid": lambda x: x.isdigit() and len(x) == 9,
}


def line_to_dict(s):
    return dict(kv.split(":") for kv in s.split(" "))


def get_lines(f):
    s = f.read()
    return [" ".join(l.split()) for l in s.split("\n\n")]


def has_all_fields(data):
    return not (ALL_FIELDS.keys() - data.keys())


def has_valid_fields(data):
    for k in data:
        if k == "cid":
            continue
        f = ALL_FIELDS[k]
        if not f(data[k]):
            # print(data, k, f(data[k]))
            return False
    return True


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    c = 0
    for line in get_lines(input):
        data = line_to_dict(line)
        if has_all_fields(data):
            c += 1
    print(c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    c = 0
    for line in get_lines(input):
        data = line_to_dict(line)
        if has_all_fields(data) and has_valid_fields(data):
            c += 1
    print(c)


if __name__ == "__main__":
    cli()
