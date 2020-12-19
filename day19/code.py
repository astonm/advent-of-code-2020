from util import *


@click.group()
def cli():
    pass


def parse_rules(lines):
    o = {}
    for line in lines:
        [ind, rule] = parse("{:d}: {}", line)
        if rule.startswith('"'):
            [rule] = parse('"{}"', rule)
        else:
            rule = [[int(y) for y in x.split()] for x in rule.split(" | ")]
        o[ind] = rule
    return o


def check_rules(rules, text):
    def _check_prefix(rule, text):
        if isinstance(rule, str):
            if text and text[0] == rule:
                return [text[1:]]
        else:
            out = []
            for option in rule:
                ways = _check_seq(option, text)
                if ways is not None:
                    out.extend(ways)
            return out

    def _check_seq(seq, text):
        ways = [text]
        for s in seq:
            next_ways = []
            for way in ways:
                subways = _check_prefix(rules[s], way)
                if subways:
                    next_ways.extend(subways)
            if not next_ways:
                return []
            ways = next_ways
        return ways

    ways = _check_prefix(rules[0], text)
    return any(w == "" for w in ways)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    rules, rest = read_file(input, delim="\n\n")
    rules = parse_rules(rules.split("\n"))

    c = 0
    for line in rest.split("\n"):
        if check_rules(rules, line):
            c += 1
    print(c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    rules, rest = read_file(input, delim="\n\n")
    rules = rules.replace("8: 42", "8: 42 | 42 8")
    rules = rules.replace("11: 42 31", "11: 42 31 | 42 11 31")
    rules = parse_rules(rules.split("\n"))

    c = 0
    for line in rest.split("\n"):
        if check_rules(rules, line):
            c += 1
    print(c)


if __name__ == "__main__":
    cli()
