from collections import Counter


def main():
    c = 0
    for line in open("input.txt"):
        spec, to_test = line.split(": ")
        if is_valid(parse_spec(spec), to_test):
            c += 1
    print(c)


def is_valid(spec, password):
    lower_match = password[spec["lower"] - 1] == spec["character"]
    upper_match = password[spec["upper"] - 1] == spec["character"]
    return lower_match ^ upper_match


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
