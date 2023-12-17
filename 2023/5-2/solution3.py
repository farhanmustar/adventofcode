import moderngl
import numpy as np
import re


with open('./test.txt', 'r') as f:
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
        maps.append([map[1], map[0], map[2], 0])
    return sorted(maps)


seeds = get_seeds(group[0])
seedToSoil = get_map('seed-to-soil map:', group[1])
soilToFertilizer = get_map('soil-to-fertilizer map:', group[2])
fertilizerToWater = get_map('fertilizer-to-water map:', group[3])
waterToLight = get_map('water-to-light map:', group[4])
lightToTemperature = get_map('light-to-temperature map:', group[5])
temperatureToHumidity = get_map('temperature-to-humidity map:', group[6])
humidityToLocation = get_map('humidity-to-location map:', group[7])


seeds_range = []
for i in range(len(seeds) // 2):
    seeds_range.append([seeds[i * 2], seeds[i * 2 + 1]])
seeds_len = sum(length for _, length in seeds_range)

with open('./solution3_compute_shader.glsl', 'r') as f:
    shader_code = f.read()

shader_code = shader_code % (
    seeds_len,
    len(seeds_range),
    len(seedToSoil),
    len(soilToFertilizer),
    len(fertilizerToWater),
    len(waterToLight),
    len(lightToTemperature),
    len(temperatureToHumidity),
    len(humidityToLocation),
)

# Initialize OpenGL context and compute shader
ctx = moderngl.create_standalone_context()
compute_shader = ctx.compute_shader(shader_code)

# Prepare input and output buffers
output_array = np.zeros(seeds_len, dtype=np.float32)
seeds_data = np.array(seeds_range, dtype=np.float32)
data = np.array(
    seedToSoil +
    soilToFertilizer +
    fertilizerToWater +
    waterToLight +
    lightToTemperature +
    temperatureToHumidity +
    humidityToLocation, dtype=np.float32)

output_buffer = ctx.buffer(output_array.tobytes())
seeds_buffer = ctx.buffer(seeds_data.tobytes())
data_buffer = ctx.buffer(data.tobytes())

output_buffer.bind_to_storage_buffer(0)
seeds_buffer.bind_to_storage_buffer(1)
data_buffer.bind_to_storage_buffer(2)

# Execute compute shader
compute_shader.run(seeds_len)

# Retrieve output data
output_buffer.bind_to_storage_buffer(0)
output_data = np.frombuffer(output_buffer.read(), dtype=np.float32)

# # Print the cube of each number
# for i, value in enumerate(output_data):
#     print(f"The cube of {i+1} is {value}")
print(min(output_data))
