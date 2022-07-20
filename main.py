import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from PIL import Image


@dataclass
class MandelbrotSet:
    max_iterations: int

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex) -> float:
        return self.escape_count(c) / self.max_iterations

    def escape_count(self, c: complex) -> int:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > 2:
                return iteration
        return self.max_iterations


# create a matrix with complex numbers
def complex_matrix(x_min, x_max, y_min, y_max, pixel_density):
    re = np.linspace(x_min, x_max, int((x_max - x_min) * pixel_density))
    im = np.linspace(y_min, y_max, int((y_max - y_min) * pixel_density))
    return re[np.newaxis, :] + im[:, np.newaxis] * 1j


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Mandelbrot()
    mandelbrot_set = MandelbrotSet(max_iterations=20)
    width, height = 1080, 1080
    scale = 0.004
    GRAYSCALE = "L"

    image = Image.new(mode=GRAYSCALE, size=(width, height))
    for y in range(height):
        for x in range(width):
            c = scale * complex(x-width/2, height/2-y)
            instability = 1 - mandelbrot_set.stability(c)
            image.putpixel((x, y), int(instability*255))

    image.show()
