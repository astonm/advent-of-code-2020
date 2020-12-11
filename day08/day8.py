import click


@click.group()
def cli():
    pass


def parsed_bytecode(input):
    out = []
    for line in input.read().strip().split("\n"):
        cmd, num = line.strip().split(" ")
        out.append((cmd, int(num)))
    return out


def run_code(code):
    pc = 0
    acc = 0
    seen = set()

    while pc < len(code):
        if pc in seen:
            return acc, False
        seen.add(pc)

        cmd, num = code[pc]
        # print(code[pc])
        if cmd == "acc":
            acc += num

        if cmd == "jmp":
            pc += num
        else:
            pc += 1
    return acc, True


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    code = parsed_bytecode(input)
    print(run_code(code))


def nop_flop_options(code):
    yield code
    for i, line in enumerate(code):
        before, after = code[:i], code[i + 1 :]
        if line[0] == "nop":
            yield before + [("jmp", line[1])] + after
        if line[0] == "jmp":
            yield before + [("nop", line[1])] + after


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    for option in nop_flop_options(parsed_bytecode(input)):
        acc, completed = run_code(option)
        if completed:
            print(acc)


if __name__ == "__main__":
    cli()
