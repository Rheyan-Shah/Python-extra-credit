from PIL import Image
import turtle
import random
import math

# ============================================================
# IMAGE SETTINGS
# ============================================================
IMAGE_PATH = (
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science"
    r"\Python\SoundDesign\imagemanipulation\input.jpg")
MAX_SIZE = 700

# ============================================================
# LOAD IMAGE
# ============================================================
image = Image.open(IMAGE_PATH)
image = image.convert("RGB")
width = image.width
height = image.height

# ============================================================
# RESIZE LARGE IMAGES
# ============================================================
# Turtle becomes extremely slow
# with very large images.
#
# Resize while keeping aspect ratio.
if width > MAX_SIZE or height > MAX_SIZE:
    scale = min(
        MAX_SIZE / width,
        MAX_SIZE / height
    )
    width = int(width * scale)
    height = int(height * scale)
    image = image.resize((width, height))

# ============================================================
# PIXEL ACCESS
# ============================================================
pixels = image.load()

# ============================================================
# TURTLE SCREEN SETUP
# ============================================================
screen = turtle.Screen()
screen.colormode(255)
screen.setup(width + 100, height + 100)
# Warm canvas background
screen.bgcolor((240, 235, 220))
turtle.tracer(0, 0)

# ============================================================
# CREATE BRUSH
# ============================================================
brush = turtle.Turtle()
brush.speed(0)
brush.hideturtle()
brush.penup()

# ============================================================
# COORDINATE CONVERSION
# ============================================================
# PIL:
# top-left origin
#
# Turtle:
# center origin
def convert_x(x):
    return x - (width / 2)

def convert_y(y):
    return (height / 2) - y

# ============================================================
# GET BRIGHTNESS
# ============================================================
# Converts RGB into
# approximate brightness.
def get_brightness(pixel):
    return (
        int(pixel[0]) +
        int(pixel[1]) +
        int(pixel[2])
    ) / 3

# ============================================================
# GET STROKE DIRECTION
# ============================================================
# Estimates image flow direction
# using nearby brightness changes.
def get_direction(x, y):
    if x <= 1 or x >= width - 2:
        return random.randint(0, 360)
    if y <= 1 or y >= height - 2:
        return random.randint(0, 360)
    left_pixel = pixels[x - 1, y]
    right_pixel = pixels[x + 1, y]
    up_pixel = pixels[x, y - 1]
    down_pixel = pixels[x, y + 1]
    horizontal_change = abs(
        get_brightness(right_pixel) -
        get_brightness(left_pixel)
    )
    vertical_change = abs(
        get_brightness(down_pixel) -
        get_brightness(up_pixel)
    )
    # Strong horizontal edge:
    # use horizontal strokes
    if horizontal_change > vertical_change:
        angle = random.randint(-20, 20)
    # Strong vertical edge:
    # use vertical strokes
    else:
        angle = random.randint(70, 110)
    # Add mild natural variation
    angle += random.randint(-10, 10)
    return angle

# ============================================================
# MODIFY COLOR
# ============================================================
# Adds small paint variation
# to avoid digital perfection.
def vary_color(color, variation):
    red = color[0]
    green = color[1]
    blue = color[2]
    red += random.randint(-variation, variation)
    green += random.randint(-variation, variation)
    blue += random.randint(-variation, variation)
    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))
    return (red, green, blue)

# ============================================================
# DRAW SINGLE STROKE
# ============================================================
# Slightly curved strokes
# feel more natural than
# perfectly straight lines.
def draw_stroke(x, y, color, angle, length, thickness):
    brush.penup()
    brush.goto(x, y)
    brush.setheading(angle)
    brush.pencolor(color)
    brush.pensize(thickness)
    brush.pendown()
    # Small curve sections
    for i in range(3):
        brush.forward(length / 3)
        brush.right(
            random.randint(-4, 4)
        )
    brush.penup()

# ============================================================
# DRAW PAINT PATCH
# ============================================================
# Real paintings use
# grouped strokes.
#
# NOT isolated lines.
#
# This creates paint masses.
def draw_paint_patch(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    for stroke in range(3):
        offset_x = random.randint(
            -thickness,
            thickness
        )
        offset_y = random.randint(
            -thickness,
            thickness
        )
        draw_stroke(
            x + offset_x,
            y + offset_y,
            color,
            angle,
            length + random.randint(-3, 3),
            thickness
        )

# ============================================================
# PAINTING LAYERS
# ============================================================
# Large strokes first.
#
# Small detail later.
#
# This mimics real painting.
layers = [
    {
        "step": 18,
        "length": 24,
        "thickness": 12,
        "color_variation": 4
    },
    {
        "step": 10,
        "length": 14,
        "thickness": 7,
        "color_variation": 6
    },
    {
        "step": 6,
        "length": 8,
        "thickness": 4,
        "color_variation": 8
    }]

# ============================================================
# PAINT IMAGE
# ============================================================
for layer in layers:
    step = layer["step"]
    length = layer["length"]
    thickness = layer["thickness"]
    color_variation = layer["color_variation"]
    print()
    print("Painting layer")
    print(layer)
    for y in range(0, height, step):
        # Offset rows slightly
        # avoids visible grids
        x_offset = random.randint(0, step)
        for x in range(x_offset, width, step):
            original_color = pixels[x, y]
            paint_color = vary_color(
                original_color,
                color_variation
            )
            angle = get_direction(x, y)
            draw_x = convert_x(x)
            draw_y = convert_y(y)
            draw_paint_patch(
                draw_x,
                draw_y,
                paint_color,
                angle,
                length,
                thickness
            )

# ============================================================
# FINISH
# ============================================================
turtle.update()
print()
print("Finished painting!")
turtle.done()
