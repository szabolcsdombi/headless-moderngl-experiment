import ModernGL
from ModernGL.ext import obj
from PIL import Image

import matrices

# Data files

vertex_data = obj.load('data/dummy.obj')
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

perspective = matrices.perspective(45.0, 1.0, 0.1, 1000.0)
lookat = matrices.lookat((-70.0, -260.0, 220.0), (0.0, 0.0, 100.0))
mvp = matrices.create_mvp(perspective, lookat)

prog.uniforms['Light'].value = (-70.0, -260.0, 220.0)
prog.uniforms['Color'].value = (1.0, 1.0, 1.0, 0.25)
prog.uniforms['Mvp'].write(mvp)

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
