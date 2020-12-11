from collections import Counter


def main():
    c = 0
    for line in open("input.txt"):
        spec, to_test = line.split(": ")
        if is_valid(parse_spec(spec), Counter(to_test)):
            c += 1
    print(c)


def is_valid(spec, counts):
    return spec["lower"] <= counts[spec["character"]] <= spec["upper"]


def parse_spec(s):
    r, c = s.split(" ")
    l, u = r.split("-")
    return {
        "lower": int(l),
        "upper": int(u),
        "character": c,
    }


if __name__ == "__main__":
    main()
