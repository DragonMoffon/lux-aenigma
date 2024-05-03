#version 330

// Player Data
in vec2 in_pos;
in vec2 in_dir;
in vec3 in_colour;

out vec2 vs_dir;
out vec3 vs_colour;

// SDF sphere data
in vec2 in_primary;
in vec2 in_secondary;
in vec2 in_tertiary;

out vec2 vs_primary;
out vec2 vs_secondary;
out vec2 vs_tertiary;

void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);

    vs_dir = in_dir;
    vs_colour = in_colour;

    vs_primary = in_primary;
    vs_secondary = in_secondary;
    vs_tertiary = in_tertiary;
}
