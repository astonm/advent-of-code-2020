from util import *


def process_line(line):
    return line


def doit(s):
    while "(" in s:
        start = s.find("(")
        c = 1
        i = start + 1
        while c and i < len(s):
            if s[i] == "(":
                c += 1
            if s[i] == ")":
                c -= 1
            i += 1
        end = i

        sub = doit(s[start + 1 : end - 1])
        s = s[:start] + str(sub) + " " + s[end + 1 :]

    parts = [x for x in s.split() if x]
    o = int(parts[0])
    for i in range(1, len(parts), 2):
        op = parts[i]
        n = int(parts[i + 1])
        if op == "+":
            o += n
        elif op == "*":
            o *= n
        else:
            assert 0, f"unkown op {op}"

    return o


def doit2(s):
    while "(" in s:
        start = s.find("(")
        c = 1
        i = start + 1
        while c and i < len(s):
            if s[i] == "(":
                c += 1
            if s[i] == ")":
                c -= 1
            i += 1
        end = i

        sub = doit2(s[start + 1 : end - 1])
        s = s[:start] + str(sub) + " " + s[end + 1 :]

    q = " ".join([x for x in s.split() if x])
    if "*" in q:
        parts = [doit2(x) for x in q.split("*")]
        return prod(parts)

    return sum(int(x) for x in q.split("+"))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    s = 0
    for line in data:
        s += doit(line)
    print(s)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    s = 0
    for line in data:
        s += doit2(line)
    print(s)


if __name__ == "__main__":
    cli()
