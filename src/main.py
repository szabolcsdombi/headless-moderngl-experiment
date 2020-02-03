import moderngl as ModernGL
from ModernGL.ext.obj import Obj
from PIL import Image
from pyrr import Matrix44


def main():
    # Data files

    vertex_data = Obj.open('data/sitting.obj').pack()
    texture_image = Image.open('data/wood.jpg')
    vertex_shader_source = open('data/shader.vert').read()
    fragment_shader_source = open('data/shader.frag').read()

    # Context creation

    ctx = ModernGL.create_standalone_context()

    # Shaders

    prog = ctx.program(vertex_shader=vertex_shader_source,
                       fragment_shader=fragment_shader_source)

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
    prog['Mvp'].write(mvp.astype('f4').tobytes())

    # Texture

    texture = ctx.texture(texture_image.size, 3, texture_image.tobytes())
    texture.build_mipmaps()

    # Vertex Buffer and Vertex Array

    vbo = ctx.buffer(vertex_data)
    vao = ctx.simple_vertex_array(
        prog, vbo, * ['in_vert', 'in_text', 'in_norm'])

    # Framebuffers

    fbo = ctx.framebuffer(
        ctx.renderbuffer((512, 512)),
        ctx.depth_renderbuffer((512, 512)),
    )

    # Rendering

    fbo.use()
    ctx.enable(ModernGL.DEPTH_TEST)
    ctx.clear(0.9, 0.9, 0.9)
    texture.use()
    vao.render()

    # Loading the image using Pillow

    data = fbo.read(components=3, alignment=1)
    img = Image.frombytes('RGB', fbo.size, data, 'raw', 'RGB', 0, -1)
    img.save('output.png')


if __name__ == '__main__':
    main()
