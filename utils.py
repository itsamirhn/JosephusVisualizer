from io import BytesIO

from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
import numpy as np


def get_image(path):
    return Image.open(path)


def get_image_data(image):
    bio = BytesIO()
    image.save(bio, format='PNG')
    return bio.getvalue()


def rotate_image(image, angle):
    return image.rotate(angle * 180 / np.pi, expand=True)


def image_tint(src, tint='#ffffff'):
    if src.mode not in ['RGB', 'RGBA']:
        raise TypeError('Unsupported source image mode: {}'.format(src.mode))
    src.load()

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")
    if not tl:
        tl = 1
    tl = float(tl)
    sr, sg, sb = map(lambda tv: tv / tl, (tr, tg, tb))

    luts = (tuple(map(lambda lr: int(lr * sr + 0.5), range(256))) +
            tuple(map(lambda lg: int(lg * sg + 0.5), range(256))) +
            tuple(map(lambda lb: int(lb * sb + 0.5), range(256))))
    l = grayscale(src)
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))
    else:
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))
        luts += tuple(range(256))

    return Image.merge(*merge_args).point(luts)
