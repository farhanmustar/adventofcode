import re

with open('./input.txt', 'r') as f:
    input = f.read().strip()

group = input.split('\n\n')


def get_seeds(l):
    assert l.startswith('seeds:')
    seeds = re.findall(r'\d+', l)
    seeds = [int(s) for s in seeds]
    return seeds


def get_map(title, g):
    assert g.startswith(title)
    lines = g.split('\n')
    maps = []
    for l in lines[1:]:
        map = re.findall(r'\d+', l)
        map = [int(m) for m in map]
        assert len(map) == 3
        maps.append([map[1], map[0], map[2]])
    return sorted(maps)


seeds = get_seeds(group[0])
seedToSoil = get_map('seed-to-soil map:', group[1])
soilToFertilizer = get_map('soil-to-fertilizer map:', group[2])
fertilizerToWater = get_map('fertilizer-to-water map:', group[3])
waterToLight = get_map('water-to-light map:', group[4])
lightToTemperature = get_map('light-to-temperature map:', group[5])
temperatureToHumidity = get_map('temperature-to-humidity map:', group[6])
humidityToLocation = get_map('humidity-to-location map:', group[7])


def translate(trans, i):
    for src, dest, r in trans:
        if i < src:
            return i
        if i > src + r - 1:
            continue
        return dest + (i - src)
    return i


seeds_range = []
for i in range(len(seeds) // 2):
    seeds_range.append([seeds[i * 2], seeds[i * 2 + 1]])

seeds_len = sum(length for _, length in seeds_range)

locations = []
print_count = 30000
count = 0
for seeds_start, length in seeds_range:
    for s in range(seeds_start, seeds_start + length):
        count += 1
        print_count += 1
        if print_count >= 30000:
            print_count = 0
            print('%s/%s   %s %%' % (
                count,
                seeds_len,
                count / seeds_len * 100
            ))
        soil = translate(seedToSoil, s)
        fert = translate(soilToFertilizer, soil)
        water = translate(fertilizerToWater, fert)
        light = translate(waterToLight, water)
        temp = translate(lightToTemperature, light)
        hum = translate(temperatureToHumidity, temp)
        loc = translate(humidityToLocation, hum)
        locations.append(loc)

locations = sorted(locations)
print(min(locations))
