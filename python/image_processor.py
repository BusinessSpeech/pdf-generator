from io import BytesIO
from PIL import Image


def make_transparent_pixels_white(image: BytesIO) -> BytesIO:
    img = Image.open(image)
    new_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0:
                new_img.putpixel((x, y), (255, 255, 255, 0))
            else:
                new_img.putpixel((x, y), pixel)

    output_bytes = BytesIO()
    new_img.save(output_bytes, format='PNG')
    output_bytes.seek(0)
    return output_bytes
