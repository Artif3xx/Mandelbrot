import matplotlib.cm
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from PIL import Image
from math import log


@dataclass
class Viewport:
    image: Image.Image
    center: complex
    width: float

    @property
    def height(self):
        return self.scale * self.image.height

    @property
    def offset(self):
        return self.center + complex(-self.width, self.height) / 2

    @property
    def scale(self):
        return self.width / self.image.width

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)


@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int

    @property
    def color(self):
        return self.viewport.image.getpixel((self.x, self.y))

    @color.setter
    def color(self, value):
        self.viewport.image.putpixel((self.x, self.y), value)

    def __complex__(self):
        return (
                complex(self.x, -self.y)
                * self.viewport.scale
                + self.viewport.offset
        )


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex, smooth=False) -> int | float:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > 2:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
        return self.max_iterations


# creates a normal image of the mandelbrot set
def image_standard():
    mandelbrot_set = MandelbrotSet(max_iterations=20, escape_radius=1000)
    width, height = 1080, 1080
    scale = 0.004
    GRAYSCALE = "L"

    image = Image.new(mode=GRAYSCALE, size=(width, height))
    for y in range(height):
        for x in range(width):
            c = scale * complex(x - width / 2, height / 2 - y)
            instability = 1 - mandelbrot_set.stability(c, smooth=True)
            image.putpixel((x, y), int(instability * 255))

    image.show()


# creates a image at the Misiurewicz Point
def image_spiral_standard(mandelbrot_set, width=1080, height=1080):
    # mandelbrot_set = MandelbrotSet(max_iterations=256, escape_radius=1000)

    spiral_image = Image.new(mode="L", size=(width, height), color=1)
    for pixel in Viewport(spiral_image, center=-0.7435 + 0.1314j, width=0.002):
        c = complex(pixel)
        instability = 1 - mandelbrot_set.stability(c, smooth=True)
        pixel.color = int(instability * 255)

    spiral_image.show()


def paint(mandelbrot_set, viewport, palette, smooth):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        index = int(min(stability * len(palette), len(palette) - 1))
        pixel.color = palette[index % len(palette)]


def denormalize(palette):
    return [tuple(int(channel * 255) for channel in color) for color in palette]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # mandelbrot_image() # creates in image of the mandelbrot set
    colormap = matplotlib.cm.get_cmap("twilight").colors
    palette = denormalize(colormap)

    width, height = 1080, 1080
    image = Image.new(mode="RGB", size=(width, height))
    mandelbrot_set = MandelbrotSet(max_iterations=512, escape_radius=1000)
    viewport = Viewport(image, center=-0.7435 + 0.1314j, width=0.002)
    paint(mandelbrot_set, viewport, palette, smooth=True)

    image.show()

