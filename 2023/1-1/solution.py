with open('./input.txt', 'r') as f:
    input = f.read().strip()

input = input.split('\n')


def get_num(word):
    for l in word:
        if l in '1234567890':
            return int(l)


def reverse(w):
    i = len(w)
    while i > 0:
        i = i - 1
        yield w[i]

sum = 0
for w in input:
    s = get_num(w)
    e = get_num(reverse(w))
    num = s * 10 + e
    sum = num + sum

print(sum)
