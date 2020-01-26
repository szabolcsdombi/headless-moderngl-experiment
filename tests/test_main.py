from PIL import Image, ImageChops, ImageFilter
import pytest
import pywt

from src.main import main


@pytest.fixture()
def fs_with_data(fs):
    fs.add_real_file("data/sitting.obj")
    fs.add_real_file("data/sitting.png")
    fs.add_real_file("data/wood.jpg")
    fs.add_real_file("data/shader.vert")
    fs.add_real_file("data/shader.frag")
    return fs


def compute_energy(img):
    _, (cH, cV, cD) = pywt.dwt2(img, 'db1')
    return (cH ** 2 + cV ** 2 + cD ** 2).sum() / img.size[0]


def test_screen(xvfb):
    assert xvfb.width == 800
    assert xvfb.height == 600
    assert xvfb.colordepth == 16


def test_main(xvfb, fs_with_data):
    main()

    # load and convert to gray
    # reference
    img_ref = Image.open("data/sitting.png").convert('LA')
    # compute/render image
    img_result = Image.open("output.png").convert('LA')

    # using blur (box or gaussian) for reducing the antialiasing differentiation
    img_ref = img_ref.filter(ImageFilter.BoxBlur(radius=4))
    img_result = img_result.filter(ImageFilter.BoxBlur(radius=4))

    diff = ImageChops.difference(img_ref, img_result)
    # evaluate difference with some energy quantification
    # not very precise and/or accurate, but enough for utest purpose
    max_energy = compute_energy(img_ref)
    diff_energy = compute_energy(diff)
    coef_error = diff_energy/max_energy
    assert coef_error <= 1e-3
