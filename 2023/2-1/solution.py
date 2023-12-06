import re

RED = 12
GREEN = 13
BLUE = 14

with open('./input.txt', 'r') as f:
    input = f.read().strip().split('\n')

sum = 0
for game in input:
    gameId, raw = re.findall(r'^Game (\d*):(.*)', game)[0]
    # set
    for s in raw.split(';'):
        red = re.findall(r'(\d*) red', s)
        if red and int(red[0]) > RED:
            break
        green = re.findall(r'(\d*) green', s)
        if green and int(green[0]) > GREEN:
            break
        blue = re.findall(r'(\d*) blue', s)
        if blue and int(blue[0]) > BLUE:
            break
    else:
        sum = sum + int(gameId)
print(sum)

# 1916 too low
