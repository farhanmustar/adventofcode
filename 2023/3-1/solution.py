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


sum = 0
for i, l in enumerate(input):
    prev_symbol = get_symbol(input[i - 1]) if i > 0 else []
    cur_symbol = get_symbol(l)
    next_symbol = get_symbol(input[i + 1]) if i < len(input) - 1 else []

    number = get_number(l)
    for idx, n in number:
        min = idx - 1
        max = idx + len(n)
        for s in prev_symbol + cur_symbol + next_symbol:
            if s >= min and s <= max:
                sum += int(n)
                break

print(sum)
