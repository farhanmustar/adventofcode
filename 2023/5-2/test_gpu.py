import numpy as np
import moderngl

# Compute shader code
compute_shader_code = """
#version 430

layout(local_size_x = 1000, local_size_y = 1, local_size_z = 1) in;

layout(std430, binding = 0) buffer OutputBuffer {
    float output_array[];
};

void main() {
    int global_id = int(gl_GlobalInvocationID.x);
    int idx = global_id + 1;

    if (global_id < 1000) {
        output_array[global_id] = idx * idx * idx;
    }
}
"""


def main():
    # Initialize OpenGL context and compute shader
    ctx = moderngl.create_standalone_context()
    compute_shader = ctx.compute_shader(compute_shader_code)

    # Prepare input and output buffers
    output_array = np.zeros(1000, dtype=np.float32)

    output_buffer = ctx.buffer(output_array.tobytes())

    output_buffer.bind_to_storage_buffer(0)

    # Execute compute shader
    compute_shader.run(1000)

    # Retrieve output data
    output_buffer.bind_to_storage_buffer(0)
    output_data = np.frombuffer(output_buffer.read(), dtype=np.float32)

    # Print the cube of each number
    for i, value in enumerate(output_data):
        print(f"The cube of {i+1} is {value}")


if __name__ == '__main__':
    main()
