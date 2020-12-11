import click


@click.group()
def cli():
    pass


def valid_sums(l, depth):
    out = set()
    subset = l[-depth:]
    for i, x in enumerate(subset):
        for y in subset[i + 1 :]:
            out.add(x + y)
    # print(subset, out)
    return out


@cli.command()
@click.argument("input", type=click.File())
@click.argument("depth", type=int)
def part1(input, depth):
    nums = []
    for ns in input:
        n = int(ns.strip())
        if len(nums) >= depth:
            if n not in valid_sums(nums, depth):
                print(n)
        nums.append(n)


@cli.command()
@click.argument("input", type=click.File())
@click.argument("target", type=int)
def part2(input, target):
    nums = [int(ns.strip()) for ns in input]
    for i in range(0, len(nums) - 2):
        for width in range(2, len(nums)):
            got = nums[i : i + width]
            if sum(got) == target:
                print(max(got) + min(got))


if __name__ == "__main__":
    cli()
