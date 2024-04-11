#version 330
// Update Delta Time
uniform float dt;
// Min and Max speeds to limit crazy behavior, and gravity and decay consts
uniform vec4 consts;
// The points to orbit around
uniform vec4 locus;
// The velocity of the points
uniform vec4 locus_vel;
// The value at which to switch locus;
uniform int count;

// The position and velocity in
in vec2 in_pos;
in vec2 in_vel;
// The position and velocity out    
out vec2 out_pos;
out vec2 out_vel;

void main() {
    // Choose which locus to focus on.
    vec2 target = gl_VertexID < count ? locus.xy : locus.zw;
    vec2 target_vel = gl_VertexID < count ? locus_vel.xy : locus_vel.zw;
    
    // Calc new acceleration and velocity;
    vec2 pos_diff = target - in_pos;
    float sqr_dist = dot(pos_diff, pos_diff);
    float acc = dt * consts.z / sqr_dist;
    vec2 vel = in_vel + normalize(pos_diff) * acc;
    
    // Take speed and decay it. We will then clamp the speed.
    // This makes no sense physically, but go with it.
    float speed = consts.w * length(vel);
    vec2 vel_dir = normalize(vel);
    vec2 final_vel = vel_dir * clamp(speed, consts.x, consts.y);
    
    // Output the results to the next buffer. These will be used in the next call.
    out_vel = final_vel;
    out_pos = in_pos + final_vel * dt;
}
