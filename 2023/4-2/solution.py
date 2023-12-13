from collections import defaultdict
import re

with open('./input.txt', 'r') as f:
    input = f.read().strip().split('\n')


def get_game(line):
    win_str, card_str = re.findall(r'^Card *\d+: ([^|]*) \| (.*)$', line)[0]
    win_num = re.findall(r'\d+', win_str)
    card_num = re.findall(r'\d+', card_str)

    win_num = set(int(n) for n in win_num)
    card_num = set(int(n) for n in card_num)
    return (win_num, card_num)


multiply = defaultdict(lambda: 1)

sum = 0
for i, l in enumerate(input, start=1):
    win_num, card_num = get_game(l)
    matching = len(win_num & card_num)
    sum += 1 + matching * multiply[i]
    for j in range(i + 1, i + matching + 1):
        multiply[j] += multiply[i]

print(sum)
