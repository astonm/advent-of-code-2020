import click


@click.group()
def cli():
    pass


def parse_rule(line):
    left, right = line.split(" bags contain ")

    def get_color(s):
        num, rest = s.strip().split(" ", 1)
        return int(num), rest.split("bag")[0].strip()

    return left, [get_color(x) for x in right.split(",") if x != "no other bags."]


def matching_subtrees(tree, test_key):
    out = 0
    for k in tree:
        if k == test_key:
            out += 1
        elif matching_subtrees(tree[k], test_key):
            out += 1

    return out


def get_rules(input):
    return [parse_rule(l) for l in input.read().strip().split("\n")]

    return tree


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    rules = get_rules(input)

    tree = {}
    for color, _ in rules:
        tree[color] = {}

    for color, contains in rules:
        for contained in contains:
            tree[color][contained[1]] = tree[contained[1]]

    print(matching_subtrees(tree, "shiny gold") - 1)


def count_bags(subtree_key, tree):
    out = 1
    for contained in tree[subtree_key]:
        n, color = contained
        out += n * count_bags(color, tree)
    return out


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    rules = get_rules(input)

    tree = {}
    for color, _ in rules:
        tree[color] = []

    for color, contains in rules:
        for num, contained in contains:
            tree[color].append((num, contained))

    print(count_bags("shiny gold", tree) - 1)


if __name__ == "__main__":
    cli()
