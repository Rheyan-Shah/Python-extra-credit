from PIL import Image
import numpy as np
import random

# ============================================================
# LOAD IMAGE
# ============================================================
# Open image
image = Image.open(
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science\Python\SoundDesign\imagemanipulation\input.jpg")

# Convert to RGB
image = image.convert("RGB")

# Convert image into array
#
# IMPORTANT:
# int32 allows negative numbers during sharpening
#
# uint8 only supports:
# 0 to 255
#
# But sharpening kernels use:
# -1 values
#
# so we need signed integers
image_array = np.array(image).astype(np.int32)

# Image size
height = image_array.shape[0]
width = image_array.shape[1]

# ============================================================
# CONVOLUTION FUNCTION
# ============================================================
# This function applies a kernel to the image.
#
# Kernel process:
#
# 1. Place kernel over pixel
# 2. Multiply nearby pixels by kernel values
# 3. Add everything together
# 4. Replace center pixel
#
# Different kernels create:
#
# blur
# sharpen
# edges
# texture
#
# This is the heart of image filtering.

def apply_kernel(input_array, kernel):
    kernel_size = len(kernel)
    offset = kernel_size // 2
    # Output image
    output = np.zeros_like(input_array).astype(np.int32)
    # Loop through image
    for row in range(offset, height - offset):
        for col in range(offset, width - offset):
            red_total = 0
            green_total = 0
            blue_total = 0
            # Loop through kernel
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    image_row = row + kr - offset
                    image_col = col + kc - offset
                    kernel_value = kernel[kr][kc]
                    pixel = input_array[image_row][image_col]
                    # Weighted sum
                    red_total += int(pixel[0]) * kernel_value
                    green_total += int(pixel[1]) * kernel_value
                    blue_total += int(pixel[2]) * kernel_value
            # Clamp values into RGB range
            red_total = max(0, min(255, int(red_total)))
            green_total = max(0, min(255, int(green_total)))
            blue_total = max(0, min(255, int(blue_total)))
            output[row][col] = (
                red_total,
                green_total,
                blue_total
            )
    return output

# ============================================================
# BLUR KERNEL
# ============================================================
# This kernel averages nearby pixels.
#
# Effect:
#
# softer image
# smoother colors
# less detail
#
# Oil paintings usually blur small details.
blur_kernel = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]]

# ============================================================
# APPLY MULTIPLE BLUR PASSES
# ============================================================
# Repeated blurring creates paint softness.
blurred = image_array
for i in range(6):
    print("Blur pass:", i + 1)
    blurred = apply_kernel(
        blurred,
        blur_kernel
    )

# ============================================================
# SHARPEN KERNEL
# ============================================================
# Sharpening restores some edges after blur.
#
# Center pixel gets stronger weight.
# Neighbor pixels get subtracted.
#
# This increases local contrast.
sharpen_kernel = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]]

# Apply sharpening
sharpened = apply_kernel(
    blurred,
    sharpen_kernel)

# ============================================================
# TEXTURE LAYER
# ============================================================
# Oil paintings are uneven.
#
# We simulate this by:
#
# randomly blending nearby colors
#
# This creates paint texture.
texture_layer = np.copy(sharpened)
for row in range(2, height - 2):
    for col in range(2, width - 2):
        random_row = row + random.randint(-2, 2)
        random_col = col + random.randint(-2, 2)
        nearby_pixel = sharpened[random_row][random_col]
        current_pixel = sharpened[row][col]
        blended_red = int(
            (
                int(current_pixel[0]) +
                int(nearby_pixel[0])
            ) / 2
        )
        blended_green = int(
            (
                int(current_pixel[1]) +
                int(nearby_pixel[1])
            ) / 2
        )
        blended_blue = int(
            (
                int(current_pixel[2]) +
                int(nearby_pixel[2])
            ) / 2
        )
        texture_layer[row][col] = (
            blended_red,
            blended_green,
            blended_blue
        )

# ============================================================
# BRUSH STROKE LAYER
# ============================================================
# This simulates dragging wet paint sideways.
#
# Colors get smeared horizontally.
#
# This creates visible stroke structure.
brush_layer = np.copy(texture_layer)
for row in range(4, height - 4):
    for col in range(4, width - 4):
        red_total = 0
        green_total = 0
        blue_total = 0
        count = 0
        # Horizontal brush stroke
        for offset in range(-4, 5):
            pixel = texture_layer[row][col + offset]
            red_total += int(pixel[0])
            green_total += int(pixel[1])
            blue_total += int(pixel[2])
            count += 1
        brush_layer[row][col] = (
            int(red_total / count),
            int(green_total / count),
            int(blue_total / count)
        )

# ============================================================
# ADD PAINT NOISE
# ============================================================
# Real paint has:
#
# bumps
# uneven pigment
# rough texture
#
# Random noise helps fake this.
for row in range(height):
    for col in range(width):
        noise = random.randint(-20, 20)
        brush_layer[row][col][0] = max(
            0,
            min(
                255,
                int(brush_layer[row][col][0]) + noise
            )
        )
        brush_layer[row][col][1] = max(
            0,
            min(
                255,
                int(brush_layer[row][col][1]) + noise
            )
        )
        brush_layer[row][col][2] = max(
            0,
            min(
                255,
                int(brush_layer[row][col][2]) + noise
            )
        )

# ============================================================
# COLOR REDUCTION
# ============================================================
# Paintings usually have:
#
# grouped colors
# fewer tiny color differences
#
# This reduces color precision.
#
# Example:
#
# 143 becomes 125
# 188 becomes 175
#
# Creates chunkier paint appearance.
final_layer = np.copy(brush_layer)
for row in range(height):
    for col in range(width):
        pixel = final_layer[row][col]
        final_layer[row][col] = (
            int(pixel[0] / 25) * 25,
            int(pixel[1] / 25) * 25,
            int(pixel[2] / 25) * 25
        )

# ============================================================
# CANVAS TEXTURE
# ============================================================
# Adds rough canvas feel.
for row in range(height):
    for col in range(width):
        texture = random.randint(-15, 15)
        final_layer[row][col][0] = max(
            0,
            min(
                255,
                int(final_layer[row][col][0]) + texture
            )
        )
        final_layer[row][col][1] = max(
            0,
            min(
                255,
                int(final_layer[row][col][1]) + texture
            )
        )
        final_layer[row][col][2] = max(
            0,
            min(
                255,
                int(final_layer[row][col][2]) + texture
            )
        )

# ============================================================
# BLEND ORIGINAL WITH PAINT
# ============================================================
# Slightly mix original colors back in.
#
# Prevents image from becoming too muddy.
for row in range(height):
    for col in range(width):
        original_pixel = image_array[row][col]
        painted_pixel = final_layer[row][col]
        final_red = int(
            0.2 * int(original_pixel[0]) +
            0.8 * int(painted_pixel[0])
        )
        final_green = int(
            0.2 * int(original_pixel[1]) +
            0.8 * int(painted_pixel[1])
        )
        final_blue = int(
            0.2 * int(original_pixel[2]) +
            0.8 * int(painted_pixel[2])
        )
        final_layer[row][col] = (
            final_red,
            final_green,
            final_blue
        )

# ============================================================
# SAVE FINAL IMAGE
# ============================================================
# Convert back into uint8 image format
final_image = Image.fromarray(
    np.uint8(final_layer))

# Save image
final_image.save("oil_painting_output.jpg")
print("Finished!")
print("Saved as oil_painting_output.jpg")
