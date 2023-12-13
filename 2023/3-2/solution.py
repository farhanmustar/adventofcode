import re

with open('./input.txt', 'r') as f:
    input = f.read().strip().split('\n')


def get_number(line):
    output = re.finditer(r'\d+', line)
    output = [(m.start(), m.group()) for m in output]
    return output


def get_symbol(line):
    output = re.finditer(r'[^\d.]+', line)
    output = [m.start() for m in output]
    return output


def get_gear(line):
    output = re.finditer(r'\*', line)
    output = [m.start() for m in output]
    return output


sum = 0
for i, l in enumerate(input):
    prev_number = get_number(input[i - 1]) if i > 0 else []
    cur_number = get_number(l)
    next_number = get_number(input[i + 1]) if i < len(input) - 1 else []

    gear = get_gear(l)
    for g in gear:
        number = []
        for idx, n in prev_number + cur_number + next_number:
            min = idx - 1
            max = idx + len(n)
            if g >= min and g <= max:
                number.append(n)
        if len(number) == 2:
            sum += int(number[0]) * int(number[1])

print(sum)
