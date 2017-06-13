# Headless 3D rendering with python

Rendering to a [Pillow](https://github.com/python-pillow/Pillow) image using [ModernGL](https://github.com/cprogrammer1994/ModernGL)

## Requirements

- [numpy](https://github.com/numpy/numpy)
- [Pillow](https://github.com/python-pillow/Pillow)
- [ModernGL](https://github.com/cprogrammer1994/ModernGL)
- [ModernGL.ext.obj](https://github.com/cprogrammer1994/ModernGL.ext.obj)

```shell
pip install -r requirements.txt
```

## Running the script

```shell
python main.py
```

## The output

[![example](https://raw.githubusercontent.com/cprogrammer1994/Headless-rendering-with-python/master/data/example.png)](https://github.com/cprogrammer1994/Headless-rendering-with-python/blob/master/data/example.png)

## The vertex shaders

```glsl
#version 330

uniform mat4 Mvp;

in vec3 in_vert;
in vec3 in_norm;
in vec3 in_text;

out vec3 v_vert;
out vec3 v_norm;
out vec3 v_text;

void main() {
	v_vert = in_vert;
	v_norm = in_norm;
	v_text = in_text;
	gl_Position = Mvp * vec4(v_vert, 1.0);
}

```

## The fragment shaders

```glsl
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

    vec3 color = texture(Texture, v_text.xy).rgb;
    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
    f_color = vec4(color * lum, 1.0);
}
```

## The model and the texture

- The model and texture was sanitized programatically.
- The texture was resized.

You can download the original artwork [here](https://www.turbosquid.com/3d-models/free-obj-mode-dummy/662719).

## Aknowledgement

The model and the texture was created by [triduza](https://www.turbosquid.com/Search/Artists/triduza). Thank you!
