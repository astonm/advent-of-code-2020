from util import *


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    mem = {}

    for line in data:
        if line.startswith("mem"):
            addr, val = parse("mem[{:d}] = {:d}", line)
            bits = bin(val)[2:]
            bits = "0" * (36 - len(bits)) + bits

            t = []
            for b, m in zip(bits[::-1], mask[::-1]):
                if m == "1":
                    t.append("1")
                elif m == "0":
                    t.append("0")
                else:
                    t.append(b)
            bits = "".join(reversed(t))

            mem[addr] = bits
        elif line.startswith("mask"):
            (mask,) = parse("mask = {}", line)
        else:
            assert 0, line

    print(sum(int(s, 2) for s in mem.values()))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    mem = {}

    for line in data:
        if line.startswith("mem"):
            addr, val = parse("mem[{:d}] = {:d}", line)
            bits = bin(val)[2:]
            addr = bin(addr)[2:]
            addr = "0" * (36 - len(addr)) + addr

            t = []
            for b, m in zip(addr[::-1], mask[::-1]):
                if m == "1":
                    t.append("1")
                elif m == "0":
                    t.append(b)
                else:
                    t.append("X")
            addr = "".join(reversed(t))

            def all_options(bits):
                parts = bits.split("X")
                needs = len(parts) - 1
                for gots in product("01", repeat=needs):
                    out = []
                    for i in range(len(gots)):
                        out.append(parts[i])
                        out.append(gots[i])
                    out.append(parts[-1])
                    yield "".join(out)

            for addr in all_options(addr):
                mem[int(addr, 2)] = bits

        elif line.startswith("mask"):
            (mask,) = parse("mask = {}", line)
        else:
            assert 0, line

    print(sum(int(s, 2) for s in mem.values()))


if __name__ == "__main__":
    cli()
