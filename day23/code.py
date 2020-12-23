from util import *
from llist import CircularDoublyLinkedList


@click.group()
def cli():
    pass


def process_line(line):
    return [int(x) for x in line.strip()]


DEBUG = 0


def dbg(*a, **k):
    if DEBUG:
        return print(*a, **k)


def run_move(cups, current_cup_ind):
    min_cup = min(cups)
    max_cup = max(cups)

    dbg(f"{cups=} before removal")
    current_cup = cups[current_cup_ind]
    dbg(f"{current_cup=}")
    next_three = [
        cups[i % len(cups)] for i in range(current_cup_ind + 1, current_cup_ind + 4)
    ]
    dbg(f"{next_three=}")

    for n in next_three:
        cups.remove(n)

    target = current_cup - 1
    dest_cup_ind = first([i for (i, c) in enumerate(cups) if c == target])
    while dest_cup_ind is None:
        target -= 1
        if target < min_cup:
            target = max_cup
        dest_cup_ind = first([i for (i, c) in enumerate(cups) if c == target])
    dest_cup = cups[dest_cup_ind]
    dbg(f"{dest_cup=}")
    dbg(f"{cups=} after removal")

    cups = cups[: dest_cup_ind + 1] + next_three + cups[dest_cup_ind + 1 :]
    current_cup_ind = first([i for (i, c) in enumerate(cups) if c == current_cup])
    next_ind = (current_cup_ind + 1) % len(cups)
    dbg("-" * 10)
    DEBUG = 0
    return cups, next_ind


def run_move_ll(cups, lookup, current, min_cup, max_cup):
    # dbg(f"{cups.values()=} before removal")
    # dbg(f"{current=}")

    pick_up = []
    for _ in range(3):
        pick_up.append(cups.remove_elem(current.next))
    # dbg(f"{pick_up=}")
    pick_up_values = set(x.data for x in pick_up)

    target = current.data
    while True:
        target = target - 1
        if target < min_cup:
            target = max_cup
        if target not in pick_up_values:
            break

    destination = lookup[target]
    # dbg(f"{destination=}")

    for cup in pick_up:
        cups.insert_after(destination, cup)
        destination = cup

    return cups, current.next


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    cups = [process_line(l) for l in read_file(input)][0]
    current = 0

    for i in range(100):
        cups, current = run_move(cups, current)

    cup_one_ind = first([i for (i, c) in enumerate(cups) if c == 1])
    start = (cup_one_ind + 1) % len(cups)
    out = cups[start:] + cups[: start - 1]
    print("".join(str(s) for s in out))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    num_moves = 10_000_000
    cup_values = [process_line(l) for l in read_file(input)][0]
    min_cup = min(cup_values)
    max_cup = 1_000_000  # 00_000

    cups = CircularDoublyLinkedList()
    lookup = {}
    for c in chain(cup_values, range(max(cup_values) + 1, max_cup + 1)):
        node = cups.append(c)
        lookup[c] = node

    current = first(cups)
    with click.progressbar(range(num_moves)) as iterations:
        for turn_number in iterations:
            cups, current = run_move_ll(
                cups, lookup, current, min_cup=min_cup, max_cup=max_cup
            )

    cup_one = lookup[1]
    print(cup_one.next.data * cup_one.next.next.data)


if __name__ == "__main__":
    cli()
