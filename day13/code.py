from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return [int(x) for x in line.split(",") if x != "x"]


def process_line2(line):
    return [(int(x), i) for (i, x) in enumerate(line.split(",")) if x != "x"]


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    time = data[0][0]
    mods = data[1]

    dist = [(-(time % m - m), m) for m in mods]
    x = min(dist)
    print(x[0] * x[1])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line2(l) for l in read_file(input)]
    buses = data[1]

    # this is hard to explain! and probably there's an easier way.
    # the idea is to inductively find the next number that satisfies our conditions
    # working with the example 17,x,13,19
    # first, the targets. we need t % 17 == 0, t % 13 == 13 - 2 == 11, and t % 19 == 19 - 3 == 16
    # t = 17 is a good start. then we look for k*17 % 13 == 11, knowing that k can range from 0 to 13.
    # a linear search finds k = 6, so now t = 17*6. to maintain our t % 17 == 0, we must keep 17, but can
    # tweak 6 to get in our next bus in without losing t % 13 == 11. 6 works, and so does adding 19, 32 ...
    # basically anything 6 + 13*x is the same % 13, so we need to search for our next magic factor x this way:
    # 17 * (6 + 13 * x) % 19 = 16. that x turns out to be 15 and the final result is:
    # t = 0 + 17 * (6 + 13 * (15 + 19*0)) = 3417
    #     x   ^^    x   ^^    xx   ^^        (carets indicate bus numbers, x's indicate found x factors)
    #
    # `mult_factors_with` takes a series of good x factors paired with the bus number and an x to try
    # basically, a generified lambda for the above form. `next_factor` then does the simple search and
    # builds the list of factors along the way. n.b. the initial bus needs an x factor of 0.
    # once we have all the factors we can evaluate them all again at x factor=0

    factors = [buses[0]]
    for bus_num, offset in buses[1:]:
        f = next_factor(factors, bus_num, bus_num - offset)
        factors.append((bus_num, f))
    print(mult_factors_with(factors, 0))


def mult_factors_with(factors_and_nums, x):
    for num, factor in factors_and_nums[::-1]:
        x *= num
        x += factor
    return x


def next_factor(factors_and_nums, mod, target):
    while target < 0:
        target += mod
    for i in range(mod):
        if mult_factors_with(factors_and_nums, i) % mod == target:
            return i
    assert "shouldn't get here", (factors_and_nums, mod, target)


@cli.command()
@click.argument("input", type=click.File())
def part3(input):
    data = [process_line2(l) for l in read_file(input)]
    buses = data[1]

    # from above:
    # t = 0 + 17 * (6 + 13 * (15 + 19*0)) = 3417
    #     x   ^^    x   ^^    xx   ^^        (carets indicate bus numbers, x's indicate found x factors)
    #
    # this is a pain to calculate because each inductive step has us redo work. rearranging a bit...
    # t = 17 * 6 + 17 * 13 * 15 + 17 * 13 * 19 * 0 = 3417
    # t = (17) * 6 + (17 * 13) * 15 + (17 * 13 * 19) * 0 = 3417
    # written this way, we see an accumulating product multiplied by our same x factors
    # an intuition behind that accumulating product is that it's the cycle length of the buses we've
    # seen so far, and that by adding any multiple of it, we retain our moduli thus far.
    # we can clearly do this sum more incrementally without repeating work, and simplify our code, too.

    cycle_len, sum_so_far = 1, 0
    for bus_num, offset in buses:
        for i in range(bus_num):
            sum_so_far += cycle_len
            if sum_so_far % bus_num == (bus_num - offset) % bus_num:
                break
        cycle_len *= bus_num
    print(sum_so_far)


if __name__ == "__main__":
    cli()
