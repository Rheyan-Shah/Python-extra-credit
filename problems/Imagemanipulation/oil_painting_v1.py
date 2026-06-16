from PIL import Image
import numpy as np
import random

# ============================================================
# STEP 1
# LOAD IMAGE
# ============================================================
# Open image
image = Image.open("input.jpg")

# Convert image to RGB mode
image = image.convert("RGB")

# Convert image into NumPy array
# This lets us access pixels like a matrix
image_array = np.array(image)

# Get image size
height = image_array.shape[0]
width = image_array.shape[1]

# ============================================================
# STEP 2
# DEFINE CONVOLUTION FUNCTION
# ============================================================
# A convolution kernel slides across the image.
# At every pixel:
#
# 1. Multiply nearby pixels with kernel values
# 2. Add everything together
# 3. Replace the center pixel with new value
#
# This creates effects like:
# blur
# sharpen
# edges
# texture

def apply_kernel(input_array, kernel):
    # Kernel size
    kernel_size = len(kernel)
    # Middle position of kernel
    offset = kernel_size // 2
    # Create empty output image
    output = np.zeros_like(input_array)
    # Loop through image pixels
    for row in range(offset, height - offset):
        for col in range(offset, width - offset):
            red_total = 0
            green_total = 0
            blue_total = 0
            # Apply kernel to neighboring pixels
            for kr in range(kernel_size):
                for kc in range(kernel_size):
                    # Position in image
                    image_row = row + kr - offset
                    image_col = col + kc - offset
                    # Kernel value
                    kernel_value = kernel[kr][kc]
                    # Pixel color
                    pixel = input_array[image_row][image_col]
                    # Multiply pixel by kernel value
                    red_total += pixel[0] * kernel_value
                    green_total += pixel[1] * kernel_value
                    blue_total += pixel[2] * kernel_value
            # Keep values inside valid RGB range
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
# STEP 3
# BLUR KERNEL
# ============================================================
# Box blur kernel
#
# This averages nearby pixels.
# Result:
# softer image
# smoother colors
# less sharp detail
#
# Every surrounding pixel contributes equally.
blur_kernel = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]]

# Apply blur multiple times
# Multiple layers create painter softness
blurred_1 = apply_kernel(image_array, blur_kernel)
blurred_2 = apply_kernel(blurred_1, blur_kernel)

# ============================================================
# STEP 4
# EDGE ENHANCEMENT
# ============================================================
# Sharpening kernel
#
# Center pixel gets stronger weight.
# Neighbor pixels get subtracted.
#
# This increases contrast around edges.
sharpen_kernel = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]]

# Apply sharpening
sharpened = apply_kernel(blurred_2, sharpen_kernel)

# ============================================================
# STEP 5
# CREATE TEXTURE LAYER
# ============================================================
# Oil paintings usually have uneven texture.
#
# We'll simulate this by:
# 1. Randomly shifting nearby colors
# 2. Mixing neighboring pixels
#
# This creates brush-like variation.
texture_layer = np.copy(sharpened)
for row in range(1, height - 1):
    for col in range(1, width - 1):
        # Random nearby pixel
        random_row = row + random.randint(-1, 1)
        random_col = col + random.randint(-1, 1)
        # Get nearby color
        nearby_pixel = sharpened[random_row][random_col]
        current_pixel = sharpened[row][col]
        # Blend colors together
        blended_red = int(
            (int(current_pixel[0]) + int(nearby_pixel[0])) / 2
        )
        blended_green = int(
            (int(current_pixel[1]) + int(nearby_pixel[1])) / 2
        )
        blended_blue = int(
            (int(current_pixel[2]) + int(nearby_pixel[2])) / 2
        )
        texture_layer[row][col] = (
            blended_red,
            blended_green,
            blended_blue
        )

# ============================================================
# STEP 6
# ADD BRUSH-LIKE STROKES
# ============================================================
# Real oil paintings have visible direction changes.
#
# We simulate this by stretching color sideways.
#
# This acts a little like dragging wet paint.
brush_layer = np.copy(texture_layer)
for row in range(2, height - 2):
    for col in range(2, width - 2):
        # Average horizontal pixels
        left_pixel = texture_layer[row][col - 1]
        center_pixel = texture_layer[row][col]
        right_pixel = texture_layer[row][col + 1]
        red = int(
            (
                int(left_pixel[0]) +
                int(center_pixel[0]) +
                int(right_pixel[0])
            ) / 3
        )
        green = int(
            (
                int(left_pixel[1]) +
                int(center_pixel[1]) +
                int(right_pixel[1])
            ) / 3
        )
        blue = int(
            (
                int(left_pixel[2]) +
                int(center_pixel[2]) +
                int(right_pixel[2])
            ) / 3
        )
        brush_layer[row][col] = (
            red,
            green,
            blue
        )

# ============================================================
# STEP 7
# FINAL COLOR BLENDING
# ============================================================
# Blend original image slightly with paint layer.
#
# This keeps some original color richness.
final_layer = np.copy(brush_layer)
for row in range(height):
    for col in range(width):
        original_pixel = image_array[row][col]
        painted_pixel = brush_layer[row][col]
        final_red = int(
            0.3 * int(original_pixel[0]) +
            0.7 * int(painted_pixel[0])
        )
        final_green = int(
            0.3 * int(original_pixel[1]) +
            0.7 * int(painted_pixel[1])
        )
        final_blue = int(
            0.3 * int(original_pixel[2]) +
            0.7 * int(painted_pixel[2])
        )
        final_layer[row][col] = (
            final_red,
            final_green,
            final_blue
        )

# ============================================================
# STEP 8
# SAVE FINAL IMAGE
# ============================================================
# Convert NumPy array back into image
final_image = Image.fromarray(
    np.uint8(final_layer))

# Save result
final_image.save("oil_painting_output.jpg")
print("Oil painting image created!")
