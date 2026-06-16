from PIL import Image
import turtle
import random

# trying to make a painting effect
# this is the image path on my computer
image_path = (
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science"
    r"\Python\SoundDesign\imagemanipulation\input.jpg")

# image was way too big before
# turtle became insanely slow
max_size = 700

# ============================================================
# LOAD IMAGE
# ============================================================
image = Image.open(image_path)
image = image.convert("RGB")
width = image.width
height = image.height

# resize image if too large
# otherwise turtle takes forever
if width > max_size or height > max_size:
    scale = min(
        max_size / width,
        max_size / height
    )
    width = int(width * scale)
    height = int(height * scale)
    image = image.resize((width, height))

# lets access pixels directly
pixels = image.load()

# ============================================================
# TURTLE SETUP
# ============================================================
screen = turtle.Screen()
# IMPORTANT
# turtle normally expects colors from 0 to 1
# this changes it to 0 to 255 RGB
screen.colormode(255)
screen.setup(width + 100, height + 100)
# warm background looked more canvas-like
screen.bgcolor((240, 235, 220))
# speeds turtle up a LOT
turtle.tracer(0, 0)

# make brush turtle
brush = turtle.Turtle()
brush.speed(0)
brush.hideturtle()
brush.penup()

# ============================================================
# CONVERT COORDINATES
# ============================================================
# PIL image:
# top left is (0,0)
#
# turtle:
# center is (0,0)
#
# so need conversion
def convert_x(x):
    return x - (width / 2)

def convert_y(y):
    return (height / 2) - y

# ============================================================
# BRIGHTNESS FUNCTION
# ============================================================
# using average RGB
# probably not the best method honestly
# but works enough
def get_brightness(pixel):
    return (
        pixel[0] +
        pixel[1] +
        pixel[2]
    ) / 3

# ============================================================
# TRYING TO DETECT IMAGE DIRECTION
# ============================================================
# idea:
#
# compare nearby pixels
#
# if left/right changes more:
# use horizontal-ish strokes
#
# if up/down changes more:
# use vertical-ish strokes
#
# not real edge detection
# but kinda works
def get_angle(x, y):
    # edge cases
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
    # horizontal-ish strokes
    if horizontal_change > vertical_change:
        angle = random.randint(-20, 20)
    # vertical-ish strokes
    else:
        angle = random.randint(70, 110)
    # tiny randomness
    angle += random.randint(-4, 4)
    return angle

# ============================================================
# KEEP RGB INSIDE RANGE
# ============================================================
def clamp(number):
    return max(0, min(255, number))

# ============================================================
# SLIGHT COLOR VARIATION
# ============================================================
# paintings are not perfect flat colors
# this adds tiny variation
def vary_color(color, amount):
    red = color[0]
    green = color[1]
    blue = color[2]
    red += random.randint(-amount, amount)
    green += random.randint(-amount, amount)
    blue += random.randint(-amount, amount)
    red = clamp(red)
    green = clamp(green)
    blue = clamp(blue)
    return (red, green, blue)

# ============================================================
# DRAW ONE BRUSH STROKE
# ============================================================
# originally used straight lines
# looked too digital
#
# slight curves looked better
def draw_stroke(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    brush.penup()
    brush.goto(x, y)
    brush.setheading(angle)
    # tiny color breakup
    # trying to imitate paint texture
    stroke_color = (
        clamp(color[0] + random.randint(-5, 5)),
        clamp(color[1] + random.randint(-5, 5)),
        clamp(color[2] + random.randint(-5, 5))
    )
    brush.pencolor(stroke_color)
    brush.pensize(thickness)
    brush.pendown()
    # draw slightly curved stroke
    for i in range(3):
        brush.forward(length / 3)
        brush.right(
            random.randint(-2, 2)
        )
    brush.penup()

# ============================================================
# DRAW SMALL GROUP OF STROKES
# ============================================================
# one line alone looked weird
# grouping strokes together
# looked more paint-like
def draw_patch(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    for i in range(2):
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
            length + random.randint(-2, 2),
            thickness
        )

# ============================================================
# DIFFERENT PAINTING LAYERS
# ============================================================
# large strokes first
# smaller strokes later
#
# kinda copying how paintings build up
layers = [
    # big messy background layer
    {
        "step": 28,
        "length": 34,
        "thickness": 18,
        "variation": 3
    },
    # large forms
    {
        "step": 20,
        "length": 24,
        "thickness": 12,
        "variation": 4
    },
    # medium detail
    {
        "step": 14,
        "length": 18,
        "thickness": 8,
        "variation": 5
    },
    # more structure
    {
        "step": 10,
        "length": 12,
        "thickness": 6,
        "variation": 6
    },
    # detail layer
    {
        "step": 7,
        "length": 8,
        "thickness": 4,
        "variation": 7
    },
    # smaller details
    {
        "step": 5,
        "length": 5,
        "thickness": 3,
        "variation": 8
    },
    # tiny details
    {
        "step": 3,
        "length": 3,
        "thickness": 2,
        "variation": 10
    }]

# ============================================================
# MAIN PAINT LOOP
# ============================================================
for layer in layers:
    print()
    print("painting new layer")
    print(layer)
    step = layer["step"]
    length = layer["length"]
    thickness = layer["thickness"]
    variation = layer["variation"]
    for y in range(0, height, step):
        # avoids obvious grid patterns
        x_offset = random.randint(0, step)
        for x in range(x_offset, width, step):
            color = pixels[x, y]
            # add slight randomness
            color = vary_color(
                color,
                variation
            )
            angle = get_angle(x, y)
            draw_x = convert_x(x)
            draw_y = convert_y(y)
            draw_patch(
                draw_x,
                draw_y,
                color,
                angle,
                length,
                thickness
            )

# ============================================================
# FINISH
# ============================================================
turtle.update()
print()
print("done")
turtle.done()
