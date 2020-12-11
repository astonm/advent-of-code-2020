nums = {int(n) for n in open("input.txt")}

for x in nums:
    for y in nums - {x}:
        z = 2020 - x - y
        if z in nums:
            print(x * y * z)
