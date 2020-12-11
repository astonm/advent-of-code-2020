nums = {int(n) for n in open("input.txt")}

for n in nums:
    if 2020 - n in nums - {n}:
        print(n * (2020 - n))
