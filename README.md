![](https://github.com/cprogrammer1994/Headless-rendering-with-python/workflows/Python%20application/badge.svg)

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

[![example](https://raw.githubusercontent.com/cprogrammer1994/Headless-rendering-with-python/master/data/sitting.png)](https://github.com/cprogrammer1994/Headless-rendering-with-python/blob/master/data/sitting.png)

## (Unit) Tests + CI

### Requirements

- [pytest](https://docs.pytest.org/en/latest/)
- [pytest-xvfb](https://pypi.org/project/pytest-xvfb/)
- [PyWavelets]( https://pywavelets.readthedocs.io/en/latest)
- [pyfakefs](https://pypi.org/project/pyfakefs/)

```shell
pip install -r requirements_dev.txt
```

### Run the tests

```shell
Headless-rendering-with-python on  master on 🐳 v19.03.5 (localhost) via py3.7.2_ubuntu-headless-ModernGL via 🐍 py3.7.2_ubuntu-headless-ModernGL 
➜ PYTHONPATH=. pytest -vvv -s --durations=0
=================================================================== test session starts ===================================================================
platform linux -- Python 3.7.2, pytest-5.3.4, py-1.8.1, pluggy-0.13.1 -- /home/latty/.pyenv/versions/3.7.2/envs/py3.7.2_ubuntu-headless-ModernGL/bin/python3.7
cachedir: .pytest_cache
rootdir: /c/Users/latty/Prog/__COMPUTER_GRAPHICS__/ubuntu-headless-ModernGL/Headless-rendering-with-python
plugins: pyfakefs-3.7.1, xvfb-1.2.0
collected 2 items                                                                                                                                         

tests/test_main.py::test_screen PASSED
tests/test_main.py::test_main libGL error: failed to create drawable
libGL error: failed to create drawable
PASSED

================================================================= slowest test durations ==================================================================
0.75s call     tests/test_main.py::test_main
0.08s setup    tests/test_main.py::test_main
0.00s teardown tests/test_main.py::test_main
0.00s setup    tests/test_main.py::test_screen
0.00s teardown tests/test_main.py::test_screen
0.00s call     tests/test_main.py::test_screen
==================================================================== 2 passed in 1.27s ====================================================================
```

### CI: Github-Action

A workflow pipeline is set for a standard python application (running flake8 and pytest):
- Workflow results can be seen here: [Headless-rendering-with-python/actions](https://github.com/yoyonel/Headless-rendering-with-python/actions)
- Pipeline configuration can be seen/modified here: [.github/workflows/pythonapp.yml](https://github.com/yoyonel/Headless-rendering-with-python/blob/master/.github/workflows/pythonapp.yml)
```yaml
name: Python application

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements_dev.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pip install pytest
        PYTHONPATH=. pytest
```

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

## The python code

```python
import ModernGL
from ModernGL.ext import obj
from PIL import Image
from pyrr import Matrix44

# Data files

vertex_data = obj.load('data/sitting.obj')
texture_image = Image.open('data/wood.jpg')
vertex_shader_source = open('data/shader.vert').read()
fragment_shader_source = open('data/shader.frag').read()

# Context creation

ctx = ModernGL.create_standalone_context()

# Shaders

vert = ctx.vertex_shader(vertex_shader_source)
frag = ctx.fragment_shader(fragment_shader_source)
prog = ctx.program([vert, frag])

# Matrices and Uniforms

perspective = Matrix44.perspective_projection(45.0, 1.0, 0.1, 1000.0)
lookat = Matrix44.look_at(
    (-85, -180, 140),
    (0.0, 0.0, 65.0),
    (0.0, 0.0, 1.0),
)

mvp = perspective * lookat

prog.uniforms['Light'].value = (-140.0, -300.0, 350.0)
prog.uniforms['Color'].value = (1.0, 1.0, 1.0, 0.25)
prog.uniforms['Mvp'].write(mvp.astype('float32').tobytes())

# Texture

texture = ctx.texture(texture_image.size, 3, texture_image.tobytes())
texture.build_mipmaps()

# Vertex Buffer and Vertex Array

vbo = ctx.buffer(vertex_data)
vao = ctx.simple_vertex_array(prog, vbo, ['in_vert', 'in_text', 'in_norm'])

# Framebuffers

fbo1 = ctx.framebuffer(ctx.renderbuffer((512, 512), samples=4))
fbo2 = ctx.framebuffer(ctx.renderbuffer((512, 512)))

# Rendering

fbo1.use()
ctx.enable(ModernGL.DEPTH_TEST)
ctx.clear(0.9, 0.9, 0.9)
texture.use()
vao.render()

# Downsampling and loading the image using Pillow

ctx.copy_framebuffer(fbo2, fbo1)
data = fbo2.read(components=3, alignment=1)
img = Image.frombytes('RGB', fbo2.size, data).transpose(Image.FLIP_TOP_BOTTOM)
img.show()
```

## The model and the texture

- The model and texture was sanitized programatically.
- The texture was resized.

You can download the original artwork [here](https://www.turbosquid.com/3d-models/free-obj-mode-dummy/662719).

## Aknowledgement

The model and the texture was created by [triduza](https://www.turbosquid.com/Search/Artists/triduza). Thank you!
