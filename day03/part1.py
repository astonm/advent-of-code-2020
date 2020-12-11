import click


class Board:
    def __init__(self, picture):
        self.lines = [l.strip() for l in picture.strip().split("\n")]
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get(self, x, y):
        x = x % self.width
        return self.lines[y][x]


@click.command()
@click.argument("input", type=click.File())
def main(input):
    board = Board(input.read())

    print(count_trees(board, (3, 1)))


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
