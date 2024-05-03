#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

uniform float player_size;

in vec2 vs_dir[];
in vec3 vs_color[];
in vec2 vs_primary[];
in vec2 vs_secondary[];
in vec2 vs_tertiary[];

out vec2 gs_dir;
out vec3 gs_color;

out vec2 gs_primary;
out vec2 gs_secondary;
out vec2 gs_tertiary;

void main() {
    // Project the center into View Space (we do this now so Lux is billboarded)
    vec3 center = (window.view * gl_in[0].gl_Position).xyz;
    float h_size = player_size / 2.0;

    // Upper Left
    gl_Position = window.projection * vec4(center + vec3(-h_size, h_size, 0.0), 1.0);
    gs_dir = vs_dir[0];
    gs_color = vs_color[0];
    gs_primary = vs_primary[0];
    gs_secondary = vs_secondary[0];
    gs_tertiary = vs_tertiary[0];
    EmitVertex();

    // Lower Left
    gl_Position = window.projection * vec4(center + vec3(-h_size, -h_size, 0.0), 1.0);
    gs_dir = vs_dir[0];
    gs_color = vs_color[0];
    gs_primary = vs_primary[0];
    gs_secondary = vs_secondary[0];
    gs_tertiary = vs_tertiary[0];
    EmitVertex();

    // Upper Right
    gl_Position = window.projection * vec4(center + vec3(h_size, h_size, 0.0), 1.0);
    gs_dir = vs_dir[0];
    gs_color = vs_color[0];
    gs_primary = vs_primary[0];
    gs_secondary = vs_secondary[0];
    gs_tertiary = vs_tertiary[0];
    EmitVertex();

    // Lower Right
    gl_Position = window.projection * vec4(center + vec3(h_size, -h_size, 0.0), 1.0);
    gs_dir = vs_dir[0];
    gs_color = vs_color[0];
    gs_primary = vs_primary[0];
    gs_secondary = vs_secondary[0];
    gs_tertiary = vs_tertiary[0];
    EmitVertex();

    EndPrimitive();
}
