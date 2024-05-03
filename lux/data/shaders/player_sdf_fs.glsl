#version 330

in vec2 gs_dir;
in vec3 gs_color;

in vec2 gs_primary;
in vec2 gs_secondary;
in vec2 gs_tertiary;

out vec4 fs_colour;

uniform float smoothing_const;
uniform float sphere_radii[3];

float smooth_min(float a, float b){
    // A smoothing function which uses a cubic polynomial similar to smooth-step

    // We want 6x the distance we start smoothing at.
    float k = smoothing_const * 6.0;

    float h = max(k - abs(a - b), 0.0) / k;

    float x = min(a, b) - h * h * h * k * (1.0 / 6.0);

    return x;
}

float sphere_sdf(vec2 origin, vec2 sphere, float radius){
    return length(sphere - origin);
}

float world_sdf(vec2 origin){
    float primary = sphere_sdf(origin, gs_primary, sphere_radii[0]) / sphere_radii[0];
    float secondary = sphere_sdf(origin, gs_secondary, sphere_radii[1]) / sphere_radii[1];
    float tertiary = sphere_sdf(origin, gs_tertiary, sphere_radii[2]) / sphere_radii[2];

    return smooth_min(tertiary, smooth_min(secondary, primary));
}

void main() {
    // Using frag coord stinks hella bad
    float w = world_sdf(gl_FragCoord.xy) < 1.0 ? 1.0 : 0.0;

    fs_colour = vec4(w, w, w, 1.0);
}
