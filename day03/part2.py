import click


class Board:
    def __init__(self, picture):
        self.lines = [l.strip() for l in picture.strip().split("\n")]
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get(self, x, y):
        x = x % self.width
        return self.lines[y][x]


def product(l):
    p = 1
    for x in l:
        p *= x
    return p


@click.command()
@click.argument("input", type=click.File())
def main(input):
    board = Board(input.read())

    step_list = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    print(product(count_trees(board, steps) for steps in step_list))


def count_trees(board, steps):
    c = 0
    x, y = 0, 0

    while y < board.height:
        if board.get(x, y) == "#":
            c += 1
        x, y = x + steps[0], y + steps[1]

    return c


if __name__ == "__main__":
    main()
