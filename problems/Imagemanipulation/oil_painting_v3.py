from PIL import Image
import numpy as np
import random
import math

# ============================================================
# LOAD IMAGE
# ============================================================
image = Image.open(
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science\Python\SoundDesign\imagemanipulation\input.jpg")
image = image.convert("RGB")
image_array = np.array(image).astype(np.int32)
height = image_array.shape[0]
width = image_array.shape[1]

# ============================================================
# APPLY KERNEL
# ============================================================
def apply_kernel(img, kernel):
    k = len(kernel)
    offset = k // 2
    output = np.zeros_like(img).astype(np.int32)
    for row in range(offset, height - offset):
        for col in range(offset, width - offset):
            red = 0
            green = 0
            blue = 0
            for kr in range(k):
                for kc in range(k):
                    pixel_row = row + kr - offset
                    pixel_col = col + kc - offset
                    pixel = img[pixel_row][pixel_col]
                    value = kernel[kr][kc]
                    red += int(pixel[0]) * value
                    green += int(pixel[1]) * value
                    blue += int(pixel[2]) * value
            output[row][col] = (
                max(0, min(255, int(red))),
                max(0, min(255, int(green))),
                max(0, min(255, int(blue)))
            )
    return output

# ============================================================
# GAUSSIAN BLUR
# ============================================================
# Better than box blur.
#
# Center pixel matters more.
#
# Creates softer natural blending.
gaussian_kernel = [
    [1/16, 2/16, 1/16],
    [2/16, 4/16, 2/16],
    [1/16, 2/16, 1/16]]

blurred = image_array
for i in range(2):
    print("Blur pass", i + 1)
    blurred = apply_kernel(
        blurred,
        gaussian_kernel
    )

# ============================================================
# SOBEL EDGE DETECTION
# ============================================================
# These kernels detect image direction.
#
# Gx:
# horizontal change
#
# Gy:
# vertical change
sobel_x = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]]
sobel_y = [
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]]

# ============================================================
# CONVERT TO GRAYSCALE
# ============================================================
gray = np.zeros((height, width)).astype(np.int32)
for row in range(height):
    for col in range(width):
        pixel = blurred[row][col]
        gray[row][col] = int(
            (
                int(pixel[0]) +
                int(pixel[1]) +
                int(pixel[2])
            ) / 3
        )

# ============================================================
# APPLY SOBEL
# ============================================================
gx = np.zeros((height, width))
gy = np.zeros((height, width))
for row in range(1, height - 1):
    for col in range(1, width - 1):
        value_x = 0
        value_y = 0
        for kr in range(3):
            for kc in range(3):
                pixel = gray[
                    row + kr - 1
                ][
                    col + kc - 1
                ]
                value_x += (
                    pixel *
                    sobel_x[kr][kc]
                )
                value_y += (
                    pixel *
                    sobel_y[kr][kc]
                )
        gx[row][col] = value_x
        gy[row][col] = value_y

# ============================================================
# DIRECTIONAL BRUSH STROKES
# ============================================================
# THIS is the important part.
#
# Brush strokes follow image direction.
#
# That creates the painted look.
paint_layer = np.copy(blurred)
stroke_length = 6
for row in range(3, height - 3):
    for col in range(3, width - 3):
        dx = gx[row][col]
        dy = gy[row][col]
        angle = math.atan2(dy, dx)
        red_total = 0
        green_total = 0
        blue_total = 0
        count = 0
        # Sample along brush direction
        for step in range(-stroke_length, stroke_length):
            sample_x = int(
                col + math.cos(angle) * step
            )
            sample_y = int(
                row + math.sin(angle) * step
            )
            if (
                sample_x >= 0 and
                sample_x < width and
                sample_y >= 0 and
                sample_y < height
            ):
                pixel = blurred[sample_y][sample_x]
                red_total += int(pixel[0])
                green_total += int(pixel[1])
                blue_total += int(pixel[2])
                count += 1
        if count > 0:
            paint_layer[row][col] = (
                int(red_total / count),
                int(green_total / count),
                int(blue_total / count)
            )

# ============================================================
# PAINT TEXTURE
# ============================================================
# Simulates uneven paint thickness.
for row in range(height):
    for col in range(width):
        texture = random.randint(-5, 5)
        paint_layer[row][col][0] = max(
            0,
            min(
                255,
                int(paint_layer[row][col][0]) + texture
            )
        )
        paint_layer[row][col][1] = max(
            0,
            min(
                255,
                int(paint_layer[row][col][1]) + texture
            )
        )
        paint_layer[row][col][2] = max(
            0,
            min(
                255,
                int(paint_layer[row][col][2]) + texture
            )
        )

# ============================================================
# COLOR QUANTIZATION
# ============================================================
# Groups colors into paint-like chunks.
for row in range(height):
    for col in range(width):
        pixel = paint_layer[row][col]
        paint_layer[row][col] = (
            int(pixel[0] / 12) * 12,
            int(pixel[1] / 12) * 12,
            int(pixel[2] / 12) * 12
        )

# ============================================================
# MILD SHARPEN
# ============================================================
# Keeps important forms visible.
sharpen_kernel = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]]
final_image_array = apply_kernel(
    paint_layer,
    sharpen_kernel)

# ============================================================
# SAVE IMAGE
# ============================================================
final_image = Image.fromarray(
    np.uint8(final_image_array))
final_image.save("oil_painting_output.png")
print("Finished!")
print("Saved as oil_painting_output.png")
