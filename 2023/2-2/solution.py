import re

with open('./input.txt', 'r') as f:
    input = f.read().strip().split('\n')

sum = 0
for game in input:
    gameId, raw = re.findall(r'^Game (\d*):(.*)', game)[0]
    # set
    r = 1
    g = 1
    b = 1
    for s in raw.split(';'):
        red = re.findall(r'(\d*) red', s)
        if red and int(red[0]) > r:
            r = int(red[0])
        green = re.findall(r'(\d*) green', s)
        if green and int(green[0]) > g:
            g = int(green[0])
        blue = re.findall(r'(\d*) blue', s)
        if blue and int(blue[0]) > b:
            b = int(blue[0])
    sum = sum + (r * g * b)
print(sum)

# 2286 too low
