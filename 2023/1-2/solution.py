with open('./input.txt', 'r') as f:
    input = f.read().strip()

input = input.split('\n')


txt_num = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_num(word):
    for i, l in enumerate(word):
        if l in '1234567890':
            return (i, int(l))


def reverse(w):
    i = len(w)
    while i > 0:
        i = i - 1
        yield w[i]


def find_min(w):
    i = 99999
    n = 0
    for num, t in enumerate(txt_num, start=1):
        idx = w.find(t)
        if idx < 0:
            continue
        if idx < i:
            i = idx
            n = num

    if i == 99999:
        i = -1
    return (i, n)


def find_max(w):
    i = -1
    n = 0
    for num, t in enumerate(txt_num, start=1):
        idx = w.rfind(t)
        if idx < 0:
            continue
        if idx > i:
            i = idx
            n = num

    return (i, n)


out = []
sum = 0
for w in input:
    si, s = get_num(w)
    ei, e = get_num(reverse(w))
    ei = len(w) - ei - 1
    tsi, ts = find_min(w)
    tei, te = find_max(w)

    option = []
    if si >= 0:
        option.append((si, s))
    if tsi >= 0:
        option.append((tsi, ts))
    if ei >= 0:
        option.append((ei, e))
    if tei >= 0:
        option.append((tei, te))

    option.sort(key=lambda d: d[0])
    _, s = option[0]
    _, e = option[-1]

    num = s * 10 + e
    out.append(num)
    sum = num + sum

output = '\n'.join('%s' % o for o in out)
# with open('output.txt', 'w') as f:
#     f.write(output)
print(sum)
