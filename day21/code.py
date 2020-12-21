from util import *


@click.group()
def cli():
    pass


def process_line(line):
    [coded, known] = parse("{} (contains {})", line)
    return set(coded.split()), set(known.split(", "))


def common(input):
    data = [process_line(l) for l in read_file(input)]
    possibles = {}

    for words, allergens in data:
        for allergen in allergens:
            if allergen not in possibles:
                possibles[allergen] = words
            else:
                possibles[allergen] = possibles[allergen].intersection(words)

    return data, possibles


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data, possibles = common(input)
    all_words = reduce(lambda x, y: x | y, [x[0] for x in data])
    possible_words = reduce(lambda x, y: x | y, possibles.values())
    impossible_words = all_words - possible_words

    c = 0
    for words, _ in data:
        c += len(words & impossible_words)

    print(impossible_words)
    print(c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data, possibles = common(input)

    while True:
        singles = [first(words) for words in possibles.values() if len(words) == 1]
        if len(singles) == len(possibles):
            break

        for single in singles:
            for words in possibles.values():
                if len(words) > 1:
                    words -= {single}

    assignments = {k: first(v) for (k, v) in possibles.items()}
    print(",".join(x[1] for x in sorted(assignments.items())))


if __name__ == "__main__":
    cli()
