#version 330

uniform sampler2D Texture;
uniform vec4 Color;
uniform vec3 Light;

in vec3 v_vert;
in vec3 v_norm;
in vec3 v_text;

out vec4 f_color;

void main() {
	float lum = dot(normalize(v_norm), normalize(v_vert - Light));
	lum = acos(lum) / 3.14159265;
	lum = clamp(lum, 0.0, 1.0);
	lum = lum * lum;
	lum = smoothstep(0.0, 1.0, lum);

	lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;

	lum = lum * 0.8 + 0.2;

	vec3 color = texture(Texture, v_text.xy).rgb;
	color = color * (1.0 - Color.a) + Color.rgb * Color.a;
	f_color = vec4(color * lum, 1.0);
}
