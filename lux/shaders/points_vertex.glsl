#version 330
uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;


in vec2 in_pos;
out vec3 color;
void main() {
    // Let's just give them a "random" color based on the vertex id
    color = vec3(
        mod(float(gl_VertexID * 100 % 11) / 10.0, 1.0),
        mod(float(gl_VertexID * 100 % 27) / 10.0, 1.0),
        mod(float(gl_VertexID * 100 % 71) / 10.0, 1.0));
    // Pass the point position to primitive assembly
    mat4 mvp = window.projection * window.view;
    gl_Position = vec4((mvp * vec4(in_pos, 0.0, 1.0)).xy, 0.0, 1.0);
}
