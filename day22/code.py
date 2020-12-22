from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return tuple([int(x) for x in line.split("\n")[1:]])


def combat(deck1, deck2):
    if deck1[0] < deck2[0]:
        deck1, deck2 = deck2, deck1
    return deck1[1:] + tuple([deck1[0], deck2[0]]), deck2[1:]


def rcombat(deck1, deck2):

    memory = set()
    while True:
        winner = None

        if (deck1, deck2) in memory:
            return (1, deck1)
        memory.add((deck1[:], deck2[:]))

        draw1, draw2 = deck1[0], deck2[0]
        deck1, deck2 = deck1[1:], deck2[1:]

        if len(deck1) >= draw1 and len(deck2) >= draw2:
            subwinner, _ = rcombat(deck1[:draw1], deck2[:draw2])

        else:
            subwinner = 1 if draw1 > draw2 else 2

        if subwinner == 1:
            deck1 = deck1 + tuple([draw1, draw2])
        else:
            deck2 = deck2 + tuple([draw2, draw1])

        if not deck1 or not deck2:
            winner = 1 if deck1 else 2

        if winner:
            winning = deck1 if winner == 1 else deck2
            return winner, winning


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    decks = [process_line(l) for l in read_file(input, "\n\n")]

    while True:
        decks = combat(*decks)
        if not decks[0] or not decks[1]:
            break

    winner = decks[0] if decks[0] else decks[1]
    print(sum((i + 1) * x for (i, x) in enumerate(winner[::-1])))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    decks = [process_line(l) for l in read_file(input, "\n\n")]
    _, winner = rcombat(*decks)
    print(sum((i + 1) * x for (i, x) in enumerate(winner[::-1])))


if __name__ == "__main__":
    cli()
