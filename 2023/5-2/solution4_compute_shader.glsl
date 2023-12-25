#version 430

layout(local_size_x = %s, local_size_y = 1, local_size_z = 1) in;

layout(std430, binding = 0) buffer OutputBuffer {
  float output_array[];
};

layout(binding = 1) buffer seedsBuffer {
  vec2 seeds[];
};

layout(std430, binding = 2) buffer dataBuffer {
  vec3 data[];
};

layout(std430, binding = 3) buffer workGroupBuffer {
  int wg_data[];
};

float get_seeds(int seeds_len, int idx) {
  int seeds_idx = 0;
  for (int i = 0; i < seeds_len; i++) {
    vec2 seeds_range = seeds[i];
    if (idx < seeds_idx + seeds_range[1])  {
      return seeds_range[0] + (idx - seeds_idx);
    }
    seeds_idx += int(seeds_range[1]);
  }
  return 0;
}

float trans_item(int start, int len, float ipt) {
  int end = start + len;
  for (int i = start; i < end; i++) {
    vec3 d = data[i];
    if (ipt < d[0]) {
      return ipt;
    }
    if (ipt > (d[0] + d[2] - 1)) {
      continue;
    }
    return d[1] + (ipt - d[0]);
  }
  return ipt;
}

float idx_to_loc(int idx) {
  int seeds_len = %s;
  int seedToSoil_len = %s;
  int soilToFertilizer_len = %s;
  int fertilizerToWater_len = %s;
  int waterToLight_len = %s;
  int lightToTemperature_len = %s;
  int temperatureToHumidity_len = %s;
  int humidityToLocation_len = %s;

  int start = 0;
  float seed = get_seeds(seeds_len, idx);
  float soil = trans_item(start, seedToSoil_len, seed);
  start += seedToSoil_len;
  float fert = trans_item(start, soilToFertilizer_len, soil);
  start += soilToFertilizer_len;
  float water = trans_item(start, fertilizerToWater_len, fert);
  start += fertilizerToWater_len;
  float light = trans_item(start, waterToLight_len, water);
  start += waterToLight_len;
  float temp = trans_item(start, lightToTemperature_len, light);
  start += lightToTemperature_len;
  float hum = trans_item(start, temperatureToHumidity_len, temp);
  start += temperatureToHumidity_len;
  float loc = trans_item(start, humidityToLocation_len, hum);
  return loc;
}

void main() {
  int global_id = int(gl_GlobalInvocationID.x);
  int wg_range = wg_data[0];
  int seeds_total = wg_data[1];

  int startIdx = global_id * wg_range;
  int endIdx = startIdx + wg_range;
  float min = -1;
  for (int i = startIdx; i <= endIdx; i++) {
    if (i >= seeds_total) {
      break;
    }
    float loc = idx_to_loc(i);
    if (min == -1 || loc < min) {
      min = loc;
    }
  }
  output_array[global_id] = min;
}
