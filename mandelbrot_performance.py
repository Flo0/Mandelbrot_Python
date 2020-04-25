import numpy as np
from PIL import Image
import time

image_width = 1280
image_height = 720
iterations = 200
save_image_afterwards = True
image_format = "PNG"
seconds_between_progress_notice = 1.5
__pixel_amount = image_width * image_height
__pixel_counter = 0
__last_notice = time.time()
thread_pool = []
zoom = 0.05
dx = 0.33
dy = 0.55


def mandelbrot(re, im):
    c0 = complex(re, im)
    z = 0
    for i in range(1, iterations):
        if abs(z) > 2:
            return toRGB(i)
        z = z ** 2 + c0
    return 0, 0, 0


def toRGB(i):
    percent_of_iter = 1.0 / iterations * i
    value = percent_of_iter * 255
    return value, value, min(255, value * 2)


def mod_x(x):
    return (x - (0.75 * image_width)) / (image_width / 4) * zoom + dx


def mod_y(y):
    return (y - (image_height / 2)) / (image_height / 2.5) * zoom + dy


def compute_row(y_value, row):
    in_mod_y = mod_y(y_value)
    for x in range(0, len(row)):
        mandel_result = mandelbrot(mod_x(x), in_mod_y)
        row[x][0] = mandel_result[0]
        row[x][1] = mandel_result[1]
        row[x][2] = mandel_result[2]


def compute_mandelbrot_sync(width, height):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(0, height):
        compute_row(y, data[y])
    return data


start = time.time()
array_sync = compute_mandelbrot_sync(image_width, image_height)
delta_sync = time.time() - start

print("Took " + str(delta_sync) + " ms for sync computation.")

img = Image.fromarray(array_sync, "RGB")
if save_image_afterwards:
    img.save(str(int(time.time())) + "." + image_format.lower(), image_format)
img.show()
