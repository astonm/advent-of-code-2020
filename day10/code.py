import click
import collections
import functools


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


def to_graph(options):
    graph = collections.defaultdict(list)
    for o in options:
        for d in [1, 2, 3]:
            if o + d in options:
                graph[o].append(o + d)
    return graph


def ways(start, end, graph):
    @functools.lru_cache(maxsize=None)
    def ways_recursive(start, end):
        c = 0
        if start == end:
            return 1
        for next_node in graph[start]:
            c += ways_recursive(next_node, end)
        return c

    return ways_recursive(start, end)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    joltages = sorted(data)
    joltages = [0] + joltages + [joltages[-1] + 3]

    diffs = []
    for j in range(1, len(joltages)):
        diffs.append(joltages[j] - joltages[j - 1])

    from collections import Counter

    c = Counter(diffs)
    print(c[1] * c[3])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    joltages = [0] + sorted(data) + [max(data) + 3]
    graph = to_graph(joltages)
    print(ways(0, joltages[-1], graph))


def read_file(input, delim=None):
    return [l.strip() for l in input.read().strip().split(delim)]


if __name__ == "__main__":
    cli()
