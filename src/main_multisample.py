import moderngl as ModernGL
from ModernGL.ext.obj import Obj
from PIL import Image
from pyrr import Matrix44

# Data files

vertex_data = Obj.open('data/sitting.obj').pack()
texture_image = Image.open('data/wood.jpg')
vertex_shader_source = open('data/shader.vert').read()
fragment_shader_source = open('data/shader.frag').read()

# Context creation

ctx = ModernGL.create_standalone_context()

# Shaders

prog = ctx.program(vertex_shader=vertex_shader_source, fragment_shader=fragment_shader_source)

# Matrices and Uniforms

perspective = Matrix44.perspective_projection(45.0, 1.0, 0.1, 1000.0)
lookat = Matrix44.look_at(
    (-85, -180, 140),
    (0.0, 0.0, 65.0),
    (0.0, 0.0, 1.0),
)

mvp = perspective * lookat

prog['Light'].value = (-140.0, -300.0, 350.0)
prog['Color'].value = (1.0, 1.0, 1.0, 0.25)
prog['Mvp'].write(mvp.astype('float32').tobytes())

# Texture

texture = ctx.texture(texture_image.size, 3, texture_image.tobytes())
texture.build_mipmaps()

# Vertex Buffer and Vertex Array

vbo = ctx.buffer(vertex_data)
vao = ctx.simple_vertex_array(prog, vbo, *['in_vert', 'in_text', 'in_norm'])

# Framebuffers

fbo1 = ctx.framebuffer(
    ctx.renderbuffer((512, 512), samples=4),
    ctx.depth_renderbuffer((512, 512), samples=4),
)

fbo2 = ctx.framebuffer(
    ctx.renderbuffer((512, 512)),
    ctx.depth_renderbuffer((512, 512)),
)

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
