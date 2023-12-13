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


bank = {}


def get_score(n):
    if n < 1:
        return 0
    if n == 1:
        return 1
    if n not in bank:
        bank[n] = get_score(n - 1) * 2

    return bank[n]


sum = 0
for i, l in enumerate(input):
    win_num, card_num = get_game(l)
    matching = len(win_num & card_num)
    score = get_score(matching)
    sum += score
print(sum)
