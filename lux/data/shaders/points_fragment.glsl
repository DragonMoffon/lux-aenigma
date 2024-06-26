#version 330

// Color passed in from the vertex shader
in vec3 color;
// The pixel we are writing to in the framebuffer
out vec4 fragColor;

void main() {
    // Fill the point
    fragColor = vec4(color, 1.0);
}
